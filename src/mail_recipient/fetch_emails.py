"""Модуль fetch_emails."""

import json
from datetime import datetime, timedelta
from email import policy
from email.parser import BytesParser

import aioimaplib
from channels.generic.websocket import AsyncWebsocketConsumer

from core.constants import (
    ALL,
    AT,
    ATTACHMENTS,
    AUTH_FAILED_ERROR_MESSAGE,
    AUTH_FAILED_LOGGER_ERROR_MESSAGE,
    BAD,
    CURRENT_GMT,
    DATE,
    DATETIME_FORMAT,
    EMAIL,
    EMAIL_LIST,
    ERROR,
    FETCH_EMAILS_COMPLETE,
    FROM,
    IMAP_DOMAIN_SERVER,
    INBOX,
    INDEX,
    MESSAGE,
    MESSAGE_ID,
    NEW_DATETIME_FORMAT,
    NO_DATA_IN_MAIL_LOGGER_ERROR_MESSAGE,
    NO_MESSAGES_TO_PROCESS_LOGGER_INFO,
    OK,
    PARSING_MAIL_LOGGER_ERROR_MESSAGE,
    RECEIVE_MAIL_ERROR_MESSAGE,
    RECEIVED,
    RFC822_FORMAT,
    SEARCH_MAILS_ERROR_MESSAGE,
    SEARCH_MAILS_LOGGER_ERROR_MESSAGE,
    SELECT_INBOX_ERROR_MESSAGE,
    SELECT_INBOX_LOGGER_ERROR_MESSAGE,
    SUBJECT,
    TEXT,
    TOTAL,
    TOTAL_EMAILS,
    TYPE,
)
from core.logging_config import setup_fetch_emails_logging
from core.utils import get_attachments_from_message, get_text_from_message
from email_account.models import EmailAccount
from mail_recipient.models import Email
from mail_recipient.save_email import save_email

fetch_emails_logger = setup_fetch_emails_logging()


async def fetch_emails(
    consumer: AsyncWebsocketConsumer,
    email_account: EmailAccount,
    host: str,
    port: str,
):
    """
    Подключение к почтовому серверу и получение данных электронных писем.

    Эта функция выполняет следующие действия:
    1. Подключается к почтовому серверу IMAP.
    2. Аутентифицирует пользователя с использованием предоставленных
    учетных данных.
    3. Выбирает папку "INBOX".
    4. Ищет все письма в папке "INBOX".
    5. Получает и обрабатывает электронные письма, сохраняя их в базу
    данных и отправляя через WebSocket.
    6. Логирует результаты выполнения.

    Атрибуты:
        consumer (AsyncWebsocketConsumer): Объект WebSocket consumer для
    отправки данных клиенту.
        email_account (EmailAccount): Объект учетной записи электронной
    почты.
        host (str): Хост для вложений.
        port (str): Порт для вложений.

    Вызывает ошибку:
        Exception: В случае ошибок аутентификации, выбора папки, поиска
    или получения писем.
    """
    imap_server = IMAP_DOMAIN_SERVER.get(
        email_account.email.split(AT)[1], None
    )
    imap = aioimaplib.IMAP4_SSL(host=imap_server)
    await imap.wait_hello_from_server()
    login_result = await imap.login(
        email_account.email, email_account.password
    )
    if login_result[0] != OK:
        fetch_emails_logger.error(
            AUTH_FAILED_LOGGER_ERROR_MESSAGE, login_result[1]
        )
        await consumer.send(
            text_data=json.dumps(
                {TYPE: ERROR, MESSAGE: AUTH_FAILED_ERROR_MESSAGE}
            )
        )
        return
    await imap.select(INDEX)
    select_result = await imap.select(INBOX)
    if select_result[0] != OK:
        fetch_emails_logger.error(
            SELECT_INBOX_LOGGER_ERROR_MESSAGE, select_result[1]
        )
        await consumer.send(
            text_data=json.dumps(
                {TYPE: ERROR, MESSAGE: SELECT_INBOX_ERROR_MESSAGE}
            )
        )
        return
    search_result = await imap.search(ALL)
    if search_result[0] != OK:
        fetch_emails_logger.error(
            SEARCH_MAILS_LOGGER_ERROR_MESSAGE, search_result[0]
        )
        await consumer.send(
            text_data=json.dumps(
                {TYPE: ERROR, MESSAGE: SEARCH_MAILS_ERROR_MESSAGE}
            )
        )
        return
    all_emails = search_result[1][0].split()
    total_emails = len(all_emails)
    await consumer.send(
        text_data=json.dumps({TYPE: TOTAL_EMAILS, TOTAL: total_emails})
    )
    for msg_id in all_emails:
        status, msg_data = await imap.fetch(msg_id.decode(), RFC822_FORMAT)
        if msg_id == b"":
            fetch_emails_logger.info(NO_MESSAGES_TO_PROCESS_LOGGER_INFO)
            continue
        if status == BAD:
            fetch_emails_logger.error(
                RECEIVE_MAIL_ERROR_MESSAGE, msg_id, msg_data[1]
            )
            continue
        if len(msg_data) < 2:
            fetch_emails_logger.error(
                NO_DATA_IN_MAIL_LOGGER_ERROR_MESSAGE, msg_id
            )
            continue
        try:
            msg = BytesParser(policy=policy.default).parsebytes(msg_data[1])
            email, attachments = await save_email(
                email=Email(
                    message_id=msg[MESSAGE_ID],
                    subject=msg[SUBJECT.title()],
                    mail_from=msg[FROM.title()],
                    date=datetime.strptime(msg[DATE.title()], DATETIME_FORMAT),
                    received=datetime.strptime(
                        msg[RECEIVED.title()]
                        .split(";")[1]
                        .strip()
                        .split(" (")[0],
                        DATETIME_FORMAT,
                    ),
                    text=get_text_from_message(msg),
                ),
                attachments=get_attachments_from_message(msg),
                email_account=email_account,
                host=host,
                port=port,
            )
            email_data = {
                SUBJECT: email.subject,
                FROM: email.mail_from,
                DATE: email.date.strftime(NEW_DATETIME_FORMAT),
                RECEIVED: email.received.strftime(NEW_DATETIME_FORMAT),
                TEXT: email.text,
                ATTACHMENTS: attachments,
            }
            await consumer.send(
                text_data=json.dumps({TYPE: EMAIL_LIST, EMAIL: [email_data]})
            )
        except IndexError as e:
            fetch_emails_logger.error(
                PARSING_MAIL_LOGGER_ERROR_MESSAGE, msg_id, str(e)
            )
            continue
    fetch_emails_logger.info(
        FETCH_EMAILS_COMPLETE, datetime.utcnow() + timedelta(hours=CURRENT_GMT)
    )
    await imap.logout()
