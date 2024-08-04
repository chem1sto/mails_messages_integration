"""Модуль fetch_emails."""

from datetime import datetime
from email import policy
from email.parser import BytesParser
from typing import Tuple

import aioimaplib

from core.constants import (
    ALL,
    AT,
    ATTACHMENTS,
    AUTH_FAILED_ERROR_MESSAGE,
    AUTH_FAILED_LOGGER_ERROR_MESSAGE,
    BAD,
    DATE,
    DATETIME_FORMAT,
    FROM,
    IMAP_DOMAIN_SERVER,
    INBOX,
    INDEX,
    MESSAGE_ID,
    NEW_DATETIME_FORMAT,
    NO_DATA_IN_MAIL_LOGGER_ERROR_MESSAGE,
    NO_MESSAGE_TO_PROCESS_LOGGER_INFO,
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
)
from core.logging_config import setup_fetch_emails_logging
from core.utils import extract_text_from_message, get_attachments_from_message
from email_account.models import EmailAccount
from mail_recipient.models import Email
from mail_recipient.save_email import save_email

fetch_emails_logger = setup_fetch_emails_logging()


async def connect_and_get_emails(
    email_account: EmailAccount,
) -> Tuple[aioimaplib.IMAP4_SSL, int, list]:
    """
    Подключение к почтовому серверу и получение данных электронных писем.

    Эта функция выполняет следующие действия:
    1. Подключается к почтовому серверу IMAP.
    2. Аутентифицирует пользователя с использованием предоставленных
    учетных данных.
    3. Выбирает папку "INBOX".
    4. Ищет все письма в папке "INBOX".
    5. Сохраняет общее количество писем и их идентификаторы.
    6. Логирует результаты выполнения.

    Аргументы:
        email_account (EmailAccount): Объект, содержащий данные учетной записи
    электронной почты.

    Возвращает:
        Tuple[aioimaplib.IMAP4_SSL, int, list]: Кортеж, содержащий:
            - Объект IMAP-соединения.
            - Количество найденных писем.
            - Список идентификаторов писем.

    Вызывает ошибку:
        aioimaplib.Error: В случае ошибки аутентификации, выбора папки или
    поиска писем.
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
        raise aioimaplib.Error(AUTH_FAILED_ERROR_MESSAGE)
    await imap.select(INDEX)
    select_result = await imap.select(INBOX)
    if select_result[0] != OK:
        fetch_emails_logger.error(
            SELECT_INBOX_LOGGER_ERROR_MESSAGE, select_result[1]
        )
        raise aioimaplib.Error(SELECT_INBOX_ERROR_MESSAGE)
    search_result = await imap.search(ALL)
    if search_result[0] != OK:
        fetch_emails_logger.error(
            SEARCH_MAILS_LOGGER_ERROR_MESSAGE, search_result[0]
        )
        raise aioimaplib.Error(SEARCH_MAILS_ERROR_MESSAGE)
    all_emails_id = search_result[1][0].split()
    return imap, len(all_emails_id), all_emails_id


async def read_email(
    imap: aioimaplib.IMAP4_SSL,
    email_account: EmailAccount,
    email_id: list,
    host: str,
    port: str,
) -> dict[str, str | list] | None:
    """
    Чтение и обработка данных электронного письма.

    Эта функция выполняет следующие действия:
    1. Получает данные письма по его идентификатору.
    2. Парсит данные письма.
    3. Извлекает текст и вложения из письма.
    4. Сохраняет письмо и вложения в базу данных.
    5. Возвращает данные письма в виде словаря.
    6. Логирует результаты выполнения.

    Аргументы:
        imap (aioimaplib.IMAP4_SSL): Объект IMAP-соединения.
        email_account (EmailAccount): Объект учетной записи электронной почты.
        email_id (list): Идентификатор письма.
        host (str): Хост для вложений.
        port (str): Порт для вложений.

    Возвращает:
        dict[str, str | list] | None: Словарь с данными письма или None в
    случае ошибки.

    Вызывает ошибку:
        Exception: В случае ошибок при получении или парсинге письма.
    """
    if email_id == b"":
        fetch_emails_logger.info(NO_MESSAGE_TO_PROCESS_LOGGER_INFO)
        return
    status, email_data = await imap.fetch(email_id.decode(), RFC822_FORMAT)
    if status == BAD:
        fetch_emails_logger.error(
            RECEIVE_MAIL_ERROR_MESSAGE, email_id, email_data[1]
        )
        return
    if len(email_data) < 2:
        fetch_emails_logger.error(
            NO_DATA_IN_MAIL_LOGGER_ERROR_MESSAGE, email_id
        )
        return
    try:
        email_decoded_data = BytesParser(policy=policy.default).parsebytes(
            email_data[1]
        )
        email, attachments = await save_email(
            email=Email(
                message_id=email_decoded_data[MESSAGE_ID],
                subject=email_decoded_data[SUBJECT.title()],
                mail_from=email_decoded_data[FROM.title()],
                date=datetime.strptime(
                    email_decoded_data[DATE.title()], DATETIME_FORMAT
                ),
                received=datetime.strptime(
                    email_decoded_data[RECEIVED.title()]
                    .split(";")[1]
                    .strip()
                    .split(" (")[0],
                    DATETIME_FORMAT,
                ),
                text=extract_text_from_message(email_decoded_data),
            ),
            attachments=get_attachments_from_message(email_decoded_data),
            email_account=email_account,
            host=host,
            port=port,
        )
        email_data = {
            MESSAGE_ID: email.message_id,
            SUBJECT: email.subject,
            FROM: email.mail_from,
            DATE: email.date.strftime(NEW_DATETIME_FORMAT),
            RECEIVED: email.received.strftime(NEW_DATETIME_FORMAT),
            TEXT: email.text,
            ATTACHMENTS: attachments,
        }
        return email_data
    except IndexError as e:
        fetch_emails_logger.error(
            PARSING_MAIL_LOGGER_ERROR_MESSAGE, email_id, str(e)
        )
    await imap.logout()
