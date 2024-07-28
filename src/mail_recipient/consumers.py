import json
from typing import Any, Coroutine

from channels.generic.websocket import AsyncWebsocketConsumer

from core.utils import fetch_emails
from email_account.models import EmailAccount


class EmailListConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer для обработки запросов, связанных с электронной почтой.

    Этот consumer подключается к WebSocket, принимает сообщения от клиентов,
    обрабатывает запросы на получение списка электронных писем и отправляет
    результаты обратно клиенту.

    Основные методы:
    - connect: Принимает WebSocket-соединение.
    - disconnect: Закрывает WebSocket-соединение.
    - receive: Обрабатывает входящие сообщения от клиента.
    """
    async def connect(self) -> Coroutine[Any, Any, None]:
        return await self.accept()

    async def disconnect(self, close_code: Any) -> Coroutine[Any, Any, None]:
        pass

    async def receive(self,
                      text_data: Any = None,
                      bytes_data: Any = None) -> Coroutine[Any, Any, None]:
        text_data_json = json.loads(text_data)
        action = text_data_json.get("action")
        if action != "fetch_emails":
            return await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'Неподдерживаемое действие: {action}'
            }))
        email = text_data_json.get('email')
        if not email:
            return await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Требуется электронная почта'
            }))
        email_account = await EmailAccount.objects.filter(email=email).afirst()
        if not email_account:
            return await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Электронная почта не найдена'
            }))
        else:
            emails = await fetch_emails(email_account)
            return await self.send(text_data=json.dumps({
                'type': 'email_list',
                'emails': emails
            }))
