import json
from typing import Any, Coroutine

from channels.generic.websocket import AsyncWebsocketConsumer

from core.constants import (
    ACTION,
    EMAIL,
    EMAIL_LIST,
    EMAIL_ACCOUNT_NOT_FOUND_ERROR_MESSAGE,
    EMAIL_ACCOUNT_NOT_FOUND_LOGGER_ERROR_MESSAGE,
    EMAIL_REQUIRED_ERROR_MESSAGE,
    EMAIL_REQUIRED_LOGGER_ERROR_MESSAGE,
    EMAIL_LOGGER_ERROR_MESSAGE,
    EMAILS,
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
    Асинхронный WebSocket consumer для обработки запросов, связанных с
    электронной почтой.

    Этот consumer подключается к WebSocket, принимает сообщения от клиентов,
    обрабатывает запросы на получение списка электронных писем и отправляет
    результаты обратно клиенту.

    Основные методы:
    - connect: Принимает WebSocket-соединение.
    - receive: Обрабатывает входящие сообщения от клиента.
    - disconnect: Закрывает WebSocket-соединение.
    """

    async def connect(self) -> Coroutine[Any, Any, None]:
        return await self.accept()

    async def receive(
        self, text_data: Any = None, bytes_data: Any = None
    ) -> Coroutine[Any, Any, None]:
        try:
            text_data_json = json.loads(text_data)
            action = text_data_json.get(ACTION)
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
            emails = await fetch_emails(
                email_account,
                host=host,
                port=str(port)
            )
            if ERROR in emails:
                consumer_logger.error(
                    EMAIL_LOGGER_ERROR_MESSAGE, email_account
                )
                raise ValueError(emails[ERROR])
            return await self.send(
                text_data=json.dumps({TYPE: EMAIL_LIST, EMAILS: emails})
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

    async def disconnect(self, close_code: Any) -> Coroutine[Any, Any, None]:
        pass
