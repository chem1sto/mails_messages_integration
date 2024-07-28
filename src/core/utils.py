import os
from email import policy
from email.parser import BytesParser
from typing import Any

import aioimaplib

from core.constants import (
    ALL,
    BAD,
    AUTH_FAILED_ERROR_MESSAGE,
    AUTH_FAILED_LOGGER_ERROR_MESSAGE,
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
    SEARCH_MAILS_ERROR_MESSAGE,
    SEARCH_MAILS_LOGGER_ERROR_MESSAGE,
    SELECT_INBOX_ERROR_MESSAGE,
    SELECT_INBOX_LOGGER_ERROR_MESSAGE,
    SUBJECT,
)
from core.logging_config import setup_fetch_emails_logging
from email_account.models import EmailAccount

fetch_emails_logging = setup_fetch_emails_logging()


def email_file_path(instance, filename):
    """Формирование пути загрузки файла, включая оригинальное название."""
    return os.path.join("email_files", instance.subject[:50], filename)


async def fetch_emails(
    email_account: EmailAccount,
) -> dict[str, str] | list[dict[str, Any]]:
    """Подключение к почтовому серверу и получение электронных писем."""
    imap_server = "imap.gmail.com"
    imap = aioimaplib.IMAP4_SSL(host=imap_server)
    await imap.wait_hello_from_server()
    login_result = await imap.login(
        email_account.email, email_account.password
    )
    if login_result[0] != OK:
        fetch_emails_logging.error(
            AUTH_FAILED_LOGGER_ERROR_MESSAGE, login_result[1]
        )
        return {ERROR: AUTH_FAILED_ERROR_MESSAGE}
    await imap.select(INDEX)
    select_result = await imap.select(INBOX)
    if select_result[0] != OK:
        fetch_emails_logging.error(
            SELECT_INBOX_LOGGER_ERROR_MESSAGE, select_result[1]
        )
        return {ERROR: SELECT_INBOX_ERROR_MESSAGE}
    search_result = await imap.search(ALL)
    if search_result[0] != OK:
        fetch_emails_logging.error(
            SEARCH_MAILS_LOGGER_ERROR_MESSAGE, search_result[0]
        )
        return {ERROR: SEARCH_MAILS_ERROR_MESSAGE}
    email_list = []
    for msg_id in search_result[1][0].split()[:10]:
        status, msg_data = await imap.fetch(msg_id.decode(), RFC822_FORMAT)
        if msg_id == b"":
            fetch_emails_logging.info(NO_MESSAGES_TO_PROCESS_LOGGER_INFO)
            return email_list
        if status == BAD:
            fetch_emails_logging.error(
                RECEIVE_MAIL_ERROR_MESSAGE, msg_id, msg_data[1]
            )
            continue
        try:
            if len(msg_data) < 2:
                fetch_emails_logging.error(
                    NO_DATA_IN_MAIL_LOGGER_ERROR_MESSAGE, msg_id
                )
                continue
            msg = BytesParser(policy=policy.default).parsebytes(msg_data[1])
            subject = msg[SUBJECT.title()]
            email_list.append({SUBJECT: subject, FROM: msg[FROM.title()]})
        except IndexError as e:
            fetch_emails_logging.error(
                PARSING_MAIL_LOGGER_ERROR_MESSAGE, msg_id, str(e)
            )
            continue
    await imap.logout()
    return email_list
