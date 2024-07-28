import json
from typing import Any, Coroutine

from channels.generic.websocket import AsyncWebsocketConsumer

from core.utils import fetch_emails
from email_account.models import EmailAccount
from core.constants import (
    ACTION,
    EMAIL,
    EMAIL_LIST,
    EMAIL_REQUIRED,
    EMAIL_NOT_FOUND,
    EMAILS,
    ERROR,
    FETCH_EMAILS,
    MESSAGE,
    RESPONSE_TIMED_OUT,
    TYPE,
    UNSUPPORTED_ACTION
)


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
                raise ValueError(UNSUPPORTED_ACTION, action)
            email = text_data_json.get(EMAIL)
            if not email:
                raise ValueError(EMAIL_REQUIRED)
            email_account = await EmailAccount.objects.filter(
                email=email
            ).afirst()
            if not email_account:
                raise ValueError(EMAIL_NOT_FOUND)
            emails = await fetch_emails(email_account)
            if ERROR in emails:
                raise ValueError(emails[ERROR])
            return await self.send(
                text_data=json.dumps({TYPE: EMAIL_LIST, EMAILS: emails})
            )
        except TimeoutError:
            return await self.send(
                text_data=json.dumps(
                    {
                        TYPE: ERROR,
                        MESSAGE: RESPONSE_TIMED_OUT,
                    }
                )
            )
        except Exception as e:
            return await self.send(
                text_data=json.dumps({TYPE: ERROR, MESSAGE: str(e)})
            )

    async def disconnect(self, close_code: Any) -> Coroutine[Any, Any, None]:
        pass
