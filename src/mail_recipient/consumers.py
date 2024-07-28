import json
from typing import Any, Coroutine

from channels.generic.websocket import AsyncWebsocketConsumer

from core.utils import fetch_emails
from email_account.models import EmailAccount


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
            action = text_data_json.get("action")
            if action != "fetch_emails":
                raise ValueError(f"Неподдерживаемое действие: {action}")
            email = text_data_json.get("email")
            if not email:
                raise ValueError("Требуется электронная почта")
            email_account = await EmailAccount.objects.filter(
                email=email
            ).afirst()
            if not email_account:
                raise ValueError("Электронная почта не найдена")
            emails = await fetch_emails(email_account)
            if "error" in emails:
                raise ValueError(emails["error"])
            return await self.send(
                text_data=json.dumps({"type": "email_list", "emails": emails})
            )
        except TimeoutError:
            return await self.send(
                text_data=json.dumps(
                    {
                        "type": "error",
                        "message": "Превышено время ожидания ответа",
                    }
                )
            )
        except Exception as e:
            return await self.send(
                text_data=json.dumps({"type": "error", "message": str(e)})
            )

    async def disconnect(self, close_code: Any) -> Coroutine[Any, Any, None]:
        pass
