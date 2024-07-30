import json
from datetime import datetime, timedelta
from email import policy
from email.parser import BytesParser

import aioimaplib
from channels.generic.websocket import AsyncWebsocketConsumer

from core.constants import (
    ATTACHMENTS,
    ALL,
    BAD,
    AUTH_FAILED_ERROR_MESSAGE,
    AUTH_FAILED_LOGGER_ERROR_MESSAGE,
    CURRENT_GMT,
    DATE,
    DATETIME_FORMAT,
    ERROR,
    EMAIL_LIST,
    EMAILS,
    FETCH_EMAILS_COMPLETE,
    FILENAME,
    FROM,
    INBOX,
    INDEX,
    MESSAGE_ID,
    NO_DATA_IN_MAIL_LOGGER_ERROR_MESSAGE,
    NO_MESSAGES_TO_PROCESS_LOGGER_INFO,
    OK,
    PARSING_MAIL_LOGGER_ERROR_MESSAGE,
    RFC822_FORMAT,
    RECEIVE_MAIL_ERROR_MESSAGE,
    RECEIVED,
    SEARCH_MAILS_ERROR_MESSAGE,
    SEARCH_MAILS_LOGGER_ERROR_MESSAGE,
    SELECT_INBOX_ERROR_MESSAGE,
    SELECT_INBOX_LOGGER_ERROR_MESSAGE,
    SUBJECT,
    TEXT,
    TYPE,
    URL,
)
from core.logging_config import setup_fetch_emails_logging
from core.utils import (
    get_text_from_message,
    get_attachments_from_message,
    serialize_datetime,
)
from email_account.models import EmailAccount
from mail_recipient.models import Email
from mail_recipient.utils import save_email_to_db

fetch_emails_logger = setup_fetch_emails_logging()


async def fetch_emails(
    consumer: AsyncWebsocketConsumer,
    email_account: EmailAccount,
    host: str,
    port: str,
):
    """
    Подключение к почтовому серверу и получение данных электронных писем для
    указанной электронной почты.
    """
    imap_server = "imap.gmail.com"
    imap = aioimaplib.IMAP4_SSL(host=imap_server)
    await imap.wait_hello_from_server()
    login_result = await imap.login(
        email_account.email, email_account.password
    )
    if login_result[0] != OK:
        fetch_emails_logger.error(
            AUTH_FAILED_LOGGER_ERROR_MESSAGE, login_result[1]
        )
        return {ERROR: AUTH_FAILED_ERROR_MESSAGE}
    await imap.select(INDEX)
    select_result = await imap.select(INBOX)
    if select_result[0] != OK:
        fetch_emails_logger.error(
            SELECT_INBOX_LOGGER_ERROR_MESSAGE, select_result[1]
        )
        return {ERROR: SELECT_INBOX_ERROR_MESSAGE}
    search_result = await imap.search(ALL)
    if search_result[0] != OK:
        fetch_emails_logger.error(
            SEARCH_MAILS_LOGGER_ERROR_MESSAGE, search_result[0]
        )
        return {ERROR: SEARCH_MAILS_ERROR_MESSAGE}
    all_emails = search_result[1][0].split()
    await consumer.send(
        text_data=json.dumps({TYPE: "total_emails", "total": len(all_emails[:100])})
    )
    for msg_id in all_emails[:100]:
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
            attachments = get_attachments_from_message(msg, host, port)
            message_id = msg[MESSAGE_ID]
            subject = msg[SUBJECT.title()]
            mail_from = msg[FROM.title()]
            date = datetime.strptime(msg[DATE.title()], DATETIME_FORMAT)
            received = datetime.strptime(
                msg[RECEIVED.title()].split(";")[1].strip().split(" (")[0],
                DATETIME_FORMAT,
            )
            text = get_text_from_message(msg)
            await save_email_to_db(
                Email(
                    message_id=message_id,
                    subject=subject,
                    mail_from=mail_from,
                    date=date,
                    received=received,
                    text=text,
                ),
                attachments,
            )
            email_data = {
                SUBJECT: subject,
                FROM: mail_from,
                DATE: serialize_datetime(date),
                RECEIVED: serialize_datetime(received),
                TEXT: text,
                ATTACHMENTS: [
                    {FILENAME: a[FILENAME], URL: a[URL]} for a in attachments
                ],
            }
            await consumer.send(
                text_data=json.dumps({TYPE: EMAIL_LIST, EMAILS: [email_data]})
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
