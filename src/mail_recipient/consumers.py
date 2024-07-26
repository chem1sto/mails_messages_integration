import asyncio
import email
from datetime import datetime

from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.timezone import make_aware
from imapclient import IMAPClient

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
        host = 'imap.gmail.com'
        username = 'vladvasiliev52@gmail.com'
        password = 'adsfdg1324youknow'
        server = IMAPClient(host, use_uid=True, ssl=True)
        server.login(username, password)
        select_info = server.select_folder('INBOX')
        print('%d messages in INBOX' % select_info['EXISTS'])
        while True:
            messages = server.search(['UNSEEN'])
            for uid, message_data in server.fetch(messages, 'RFC822').items():
                email_message = email.message_from_bytes(
                    message_data[b'RFC822']
                )
                subject = email_message['Subject']
                sender = email_message['From']
                date = make_aware(datetime.strptime(
                    email_message['Date'], '%a, %d %b %Y %H:%M:%S %z')
                )
                body = email_message.get_payload(decode=True).decode()
                Email.objects.create(
                    subject=subject, sender=sender, date=date, body=body
                )
                await self.send(text_data=subject)
            await asyncio.sleep(10)  # Проверка новых писем каждые 10 секунд
        server.logout()
