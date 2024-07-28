import json
from channels.generic.websocket import AsyncWebsocketConsumer
from core.utils import (
    fetch_emails,
)  # Замените на имя вашего модуля с функцией fetch_emails
from email_account.models import EmailAccount


class EmailListConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get("action")

        if action == "fetch_emails":
            email_accounts = EmailAccount.objects.filter(
                user=self.scope["user"]
            )
            emails = []

            for account in email_accounts:
                emails.extend(await fetch_emails(account))

            await self.send(
                text_data=json.dumps(
                    {
                        "type": "email_list",
                        "emails": emails,
                    }
                )
            )
