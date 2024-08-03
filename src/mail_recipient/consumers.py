"""Модуль consumers."""

import asyncio
import json
from typing import Any, Coroutine

from channels.generic.websocket import AsyncWebsocketConsumer

from core.constants import (
    ACTION,
    CLOSE_CONNECTION,
    EMAIL,
    EMAIL_ACCOUNT_NOT_FOUND_ERROR_MESSAGE,
    EMAIL_ACCOUNT_NOT_FOUND_LOGGER_ERROR_MESSAGE,
    EMAIL_REQUIRED_ERROR_MESSAGE,
    EMAIL_REQUIRED_LOGGER_ERROR_MESSAGE,
    ERROR,
    FETCH_EMAILS,
    MESSAGE,
    SERVER,
    TIMEOUT_ERROR_MESSAGE,
    TIMEOUT_LOGGER_ERROR_MESSAGE,
    TYPE,
    UNEXPECTED_LOGGER_ERROR_MESSAGE,
    UNSUPPORTED_ACTION_ERROR_MESSAGE,
    UNSUPPORTED_ACTION_LOGGER_ERROR_MESSAGE,
)
from core.logging_config import setup_consumer_logging
from email_account.models import EmailAccount
from mail_recipient.fetch_emails import fetch_emails

consumer_logger = setup_consumer_logging()


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
    ) -> Coroutine[Any, Any, None] | None:
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
            host, port = self.scope[SERVER]
            self.fetch_task = asyncio.create_task(
                fetch_emails(
                    consumer=self,
                    email_account=email_account,
                    host=host,
                    port=str(port),
                )
            )
        except TimeoutError:
            consumer_logger.error(TIMEOUT_LOGGER_ERROR_MESSAGE, exc_info=True)
            return await self.send(
                text_data=json.dumps(
                    {
                        TYPE: ERROR,
                        MESSAGE: TIMEOUT_ERROR_MESSAGE,
                    }
                )
            )
        except Exception as e:
            consumer_logger.error(
                UNEXPECTED_LOGGER_ERROR_MESSAGE, str(e), exc_info=True
            )
            return await self.send(
                text_data=json.dumps({TYPE: ERROR, MESSAGE: str(e)})
            )

    async def disconnect(self, close_code: Any) -> None:
        """
        Закрывает WebSocket-соединение.

        Этот метод вызывается при закрытии соединения с клиентом.
        Он завершает соединение и выполняет необходимые действия по очистке.

        Аргументы:
            close_code (Any): Код закрытия соединения.

        Возвращает:
            Coroutine[Any, Any, None]: Асинхронная корутина.
        """
        if self.fetch_task:
            self.fetch_task.cancel()
        await self.close(close_code)
