import asyncio
import email
from datetime import datetime

from aioimaplib import aioimaplib
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.timezone import make_aware

from mail_recipient.models import Email


class EmailConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        asyncio.create_task(self.fetch_emails())

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass

    async def fetch_emails(self):
        host = "imap.gmail.com"
        username = "vladvasiliev52@gmail.com"  # Используйте переменные окружения или секреты Django
        password = "adsfdg1324youknow"  # Используйте переменные окружения или секреты Django

        try:
            server = aioimaplib.IMAP4_SSL(host=host)
            await server.wait_hello_from_server()
            await server.login(username, password)
            await server.select("INBOX")

            while True:
                await server.idle()
                response = await server.search("UNSEEN")
                messages = response[1][0].split()

                for msg_id in messages:
                    response = await server.fetch(msg_id, "(RFC822)")
                    email_message = email.message_from_bytes(response[1][0][1])
                    subject = email_message["Subject"]
                    sender = email_message["From"]
                    date = make_aware(
                        datetime.strptime(
                            email_message["Date"], "%a, %d %b %Y %H:%M:%S %z"
                        )
                    )
                    body = email_message.get_payload(decode=True).decode()

                    Email.objects.create(
                        subject=subject, sender=sender, date=date, body=body
                    )
                    await self.send(text_data=subject)

                await asyncio.sleep(
                    10
                )  # Проверка новых писем каждые 10 секунд
        except Exception as e:
            logger.error("Error fetching emails: %s", e)
        finally:
            await server.logout()
