"""Модуль consumers."""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Any, Coroutine

import aioimaplib
from channels.generic.websocket import AsyncWebsocketConsumer
from core.constants import (
    ACTION,
    ALL_EMAILS_ID_RECEIVED_LOGGER_INFO,
    CHECKED,
    CHECKED_EMAIL_LOGGER_INFO_MESSAGE,
    CLOSE_CONNECTION,
    CURRENT_GMT,
    EMAIL,
    EMAIL_ACCOUNT_NOT_FOUND_ERROR_MESSAGE,
    EMAIL_ACCOUNT_NOT_FOUND_LOGGER_ERROR_MESSAGE,
    EMAIL_DATA,
    EMAIL_DATA_SEND_LOGGER_MESSAGE,
    EMAIL_REQUIRED_ERROR_MESSAGE,
    EMAIL_REQUIRED_LOGGER_ERROR_MESSAGE,
    ERROR,
    FETCH_EMAILS,
    FETCH_EMAILS_CANCELLED_LOGGER_MESSAGE,
    FETCH_EMAILS_COMPLETE_LOGGER_MESSAGE,
    MESSAGE,
    MESSAGE_ID,
    NEW_EMAIL,
    PROGRESS,
    TIMEOUT_ERROR_MESSAGE,
    TIMEOUT_LOGGER_ERROR_MESSAGE,
    TOTAL,
    TOTAL_EMAILS,
    TYPE,
    UNEXPECTED_LOGGER_ERROR_MESSAGE,
    UNSUPPORTED_ACTION_ERROR_MESSAGE,
    UNSUPPORTED_ACTION_LOGGER_ERROR_MESSAGE,
)
from email_account.models import EmailAccount
from mail_recipient.fetch_emails import (
    check_email,
    connect_and_get_emails,
    read_email,
)

consumer_logger = logging.getLogger("consumer")


class EmailListConsumer(AsyncWebsocketConsumer):
    """
    Асинхронный WebSocket consumer для обработки запросов.

    Этот consumer подключается к WebSocket, принимает сообщения от клиентов,
    обрабатывает запросы на получение списка электронных писем и отправляет
    результаты обратно клиенту.

    Основные методы:
    - connect: Принимает WebSocket-соединение.
    - receive: Обрабатывает входящие сообщения от клиента.
    - disconnect: Закрывает WebSocket-соединение.
    - process_email: Обрабатывает и отправляет данные электронных писем
    клиенту.
    """

    def __init__(self, *args, **kwargs):
        """
        Инициализация экземпляра EmailListConsumer.

        Инициализирует атрибут для хранения задачи выборки электронных писем.
        """
        super().__init__(*args, **kwargs)
        self.fetch_task = None

    async def connect(self) -> Coroutine[Any, Any, None]:
        """
        Принимает WebSocket-соединение.

        Этот метод вызывается при установлении соединения с клиентом.
        Он принимает соединение и подготавливает consumer для обработки
        сообщений.
        """
        return await self.accept()

    async def receive(
        self, text_data: Any = None, bytes_data: Any = None
    ) -> None:
        """
        Обрабатывает входящие сообщения от клиента.

        Этот метод вызывается при получении сообщения от клиента.
        Он обрабатывает сообщение, проверяет наличие необходимых данных и
        выполняет соответствующие действия, такие как получение списка
        электронных писем.

        Аргументы:
            text_data (Any): Текстовые данные, полученные от клиента.
            bytes_data (Any): Байтовые данные, полученные от клиента (не
        используются в этом методе).

        Возвращает:
            Coroutine[Any, Any, None]: Асинхронная корутина.

        Вызывает ошибку:
            ValueError: Если действие не поддерживается, email не указан или
        учетная запись не найдена.
            TimeoutError: Если возникает ошибка таймаута.
            Exception: Если возникает неожиданная ошибка.
        """
        try:
            text_data_json = json.loads(text_data)
            action = text_data_json.get(ACTION)
            if action == CLOSE_CONNECTION:
                await self.close()
                return
            if action != FETCH_EMAILS:
                consumer_logger.error(
                    UNSUPPORTED_ACTION_LOGGER_ERROR_MESSAGE, action
                )
                raise ValueError(UNSUPPORTED_ACTION_ERROR_MESSAGE, action)
            email = text_data_json.get(EMAIL)
            if not email:
                consumer_logger.error(
                    EMAIL_REQUIRED_LOGGER_ERROR_MESSAGE, email
                )
                raise ValueError(EMAIL_REQUIRED_ERROR_MESSAGE)
            email_account = await EmailAccount.objects.filter(
                email=email
            ).afirst()
            if not email_account:
                consumer_logger.error(
                    EMAIL_ACCOUNT_NOT_FOUND_LOGGER_ERROR_MESSAGE, email_account
                )
                raise ValueError(EMAIL_ACCOUNT_NOT_FOUND_ERROR_MESSAGE)
            imap, total_emails, emails_id = await connect_and_get_emails(
                email_account=email_account,
            )
            await self.send(
                text_data=json.dumps({TYPE: TOTAL_EMAILS, TOTAL: total_emails})
            )
            consumer_logger.info(ALL_EMAILS_ID_RECEIVED_LOGGER_INFO)
            self.fetch_task = asyncio.create_task(
                self.process_email(
                    imap=imap, email_account=email_account, emails_id=emails_id
                )
            )
        except TimeoutError:
            consumer_logger.error(TIMEOUT_LOGGER_ERROR_MESSAGE, exc_info=True)
            return await self.send(
                text_data=json.dumps(
                    {TYPE: ERROR, MESSAGE: TIMEOUT_ERROR_MESSAGE}
                )
            )
        except Exception as e:
            consumer_logger.error(
                UNEXPECTED_LOGGER_ERROR_MESSAGE, str(e), exc_info=True
            )
            return await self.send(
                text_data=json.dumps({TYPE: ERROR, MESSAGE: str(e)})
            )

    async def disconnect(self, close_code: int) -> None:
        """
        Закрывает WebSocket-соединение.

        Этот метод вызывается при закрытии соединения с клиентом.
        Он завершает соединение и выполняет необходимые действия по очистке.

        Аргументы:
            close_code (int): Код закрытия соединения.
        """
        if self.fetch_task:
            self.fetch_task.cancel()
        await self.close(close_code)

    async def process_email(
        self,
        imap: aioimaplib.IMAP4_SSL,
        email_account: EmailAccount,
        emails_id: list,
    ) -> None:
        """
        Обрабатывает и отправляет данные электронных писем клиенту.

        Этот метод вызывается для каждого идентификатора электронного письма
        и отправляет данные письма обратно клиенту через WebSocket.

        Аргументы:
            imap: Объект IMAP-соединения.
            email_account: Учетная запись электронной почты.
            emails_id: Список идентификаторов электронных писем.
            host: Хост сервера.
            port: Порт сервера.
        """
        try:
            checked_emails_data = []
            checked_email_counter = 0
            for email_id in emails_id:
                checked_email_data = await check_email(imap, email_id)
                checked_emails_data.append(checked_email_data)
                checked_email_counter += 1
                consumer_logger.info(
                    CHECKED_EMAIL_LOGGER_INFO_MESSAGE, email_id
                )
                await self.send(
                    text_data=json.dumps(
                        {TYPE: PROGRESS, CHECKED: checked_email_counter}
                    )
                )
            for checked_email_data in checked_emails_data:
                email_data = await read_email(
                    imap=imap,
                    email_account=email_account,
                    email_data=checked_email_data,
                )
                await self.send(
                    text_data=json.dumps(
                        {TYPE: NEW_EMAIL, EMAIL_DATA: email_data}
                    )
                )
                consumer_logger.info(
                    EMAIL_DATA_SEND_LOGGER_MESSAGE, email_data.get(MESSAGE_ID)
                )
        except asyncio.CancelledError:
            consumer_logger.info(FETCH_EMAILS_CANCELLED_LOGGER_MESSAGE)
        except Exception as e:
            consumer_logger.error(
                UNEXPECTED_LOGGER_ERROR_MESSAGE, str(e), exc_info=True
            )
        finally:
            consumer_logger.info(
                FETCH_EMAILS_COMPLETE_LOGGER_MESSAGE,
                datetime.utcnow() + timedelta(hours=CURRENT_GMT),
            )
