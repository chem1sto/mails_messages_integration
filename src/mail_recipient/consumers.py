import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from imapclient import IMAPClient
import email


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
        username = 'your-email@gmail.com'  # Ваш адрес Gmail
        password = 'your-app-password'  # Пароль приложения, созданный ранее

        server = IMAPClient(host, use_uid=True, ssl=True)
        server.login(username, password)
        select_info = server.select_folder('INBOX')
        print('%d messages in INBOX' % select_info['EXISTS'])

        while True:
            messages = server.search(['UNSEEN'])
            for uid, message_data in server.fetch(messages, 'RFC822').items():
                email_message = email.message_from_bytes(message_data[b'RFC822'])
                await self.send(text_data=email_message['Subject'])
            await asyncio.sleep(10)  # Проверка новых писем каждые 10 секунд

        server.logout()
