from email import policy
from email.parser import BytesParser
from typing import Any

import aioimaplib
from django.core.files import File

from core.constants import (
    ATTACHMENTS,
    ALL,
    BAD,
    AUTH_FAILED_ERROR_MESSAGE,
    AUTH_FAILED_LOGGER_ERROR_MESSAGE,
    DATE,
    ERROR,
    FROM,
    INBOX,
    INDEX,
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
)
from core.logging_config import setup_fetch_emails_logging
from core.utils import (
    email_file_path, get_text_from_message, get_attachments_from_message
)
from email_account.models import EmailAccount
from mail_recipient.models import Email

fetch_emails_logger = setup_fetch_emails_logging()


async def fetch_emails(
    email_account: EmailAccount,
) -> dict[str, str] | list[dict[str, Any]]:
    """
    Подключение к почтовому серверу и получение данных электронных писем для
    полученной электронной почты с сохранением в БД.
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
    email_list = []
    for msg_id in search_result[1][0].split()[:10]:
        status, msg_data = await imap.fetch(msg_id.decode(), RFC822_FORMAT)
        if msg_id == b"":
            fetch_emails_logger.info(NO_MESSAGES_TO_PROCESS_LOGGER_INFO)
            return email_list
        if status == BAD:
            fetch_emails_logger.error(
                RECEIVE_MAIL_ERROR_MESSAGE, msg_id, msg_data[1]
            )
            continue
        try:
            if len(msg_data) < 2:
                fetch_emails_logger.error(
                    NO_DATA_IN_MAIL_LOGGER_ERROR_MESSAGE, msg_id
                )
                continue
            msg = BytesParser(policy=policy.default).parsebytes(msg_data[1])
            subject = msg[SUBJECT.title()]
            date = msg[DATE.title()]
            received = msg[RECEIVED.title()]
            text = get_text_from_message(msg)
            attachments = get_attachments_from_message(msg)
            email = Email(
                subject=subject,
                mail_from=msg[FROM.title()],
                date=date,
                received=received,
                text=text,
            )
            email.save()
            for attachment in attachments:
                filename = attachment["filename"]
                content = attachment["content"]
                with open(email_file_path(email, filename), "wb") as f:
                    f.write(content)
                email.attachments.save(filename, File(f))
            email_list.append(
                {
                    SUBJECT: subject,
                    FROM: msg[FROM.title()],
                    DATE: date,
                    RECEIVED: received,
                    TEXT: text,
                    ATTACHMENTS: attachments,
                }
            )
        except IndexError as e:
            fetch_emails_logger.error(
                PARSING_MAIL_LOGGER_ERROR_MESSAGE, msg_id, str(e)
            )
            continue
    await imap.logout()
    return email_list
