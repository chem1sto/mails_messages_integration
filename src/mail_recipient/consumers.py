import json
from channels.generic.websocket import AsyncWebsocketConsumer
from core.utils import fetch_emails
from email_account.models import EmailAccount


class EmailListConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json.get("action") == "fetch_emails":
            email = text_data_json.get('email')
            if email:
                email_account = await EmailAccount.objects.filter(email=email).afirst()
                if email_account:
                    emails = await fetch_emails(email_account)
                    await self.send(text_data=json.dumps({
                        'type': 'email_list',
                        'emails': emails
                    }))
                else:
                    await self.send(text_data=json.dumps({
                        'type': 'error',
                        'message': 'Email account not found'
                    }))
            else:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'Email is required'
                }))
