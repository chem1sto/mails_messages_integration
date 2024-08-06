"""Модуль save_email."""

import logging
import os

from asgiref.sync import sync_to_async
from core.constants import (
    CONTENT,
    DATE,
    FILENAME,
    MAIL_FROM,
    NO_SUBJECT,
    RECEIVED,
    SAVE_EMAIL_ATTACHMENTS_TO_DB_SUCCESS,
    SAVE_EMAIL_TO_DB,
    SAVE_EMAIL_TO_DB_SUCCESS,
    SUBJECT,
    TEXT,
    URL,
    AttachmentConfig,
)
from core.utils import generate_subfolder_name, sanitize_and_truncate_filename
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from email_account.models import EmailAccount
from mail_recipient.models import Attachment, Email

save_email_to_db_logger = logging.getLogger(SAVE_EMAIL_TO_DB)


async def save_email(
    email: Email,
    attachments: list,
    email_account: EmailAccount,
) -> tuple[Email, list]:
    """
    Сохранение электронного письма в базу данных и на локальный диск.

    Эта функция выполняет следующие действия:
    1. Создает или обновляет запись электронного письма в базе данных.
    2. Сохраняет вложения письма на локальный диск и создает записи о них в
    базе данных.
    3. Возвращает объект Email и список вложений с URL.

    Аргументы:
        email (Email): Объект электронного письма, содержащий данные для
    сохранения.
        attachments (list): Список вложений письма, где каждое вложение
    представлено словарем с ключами FILENAME и CONTENT.
        email_account (EmailAccount): Объект учетной записи электронной почты,
    от имени которой сохраняется письмо.

    Возвращает:
        tuple[Email, list]: Кортеж, содержащий:
            - Объект Email, сохраненный в базе данных.
            - Список вложений с URL, где каждое вложение представлено словарем
        с ключами FILENAME и URL.
    """
    if not email.subject:
        email.subject = NO_SUBJECT
    email_instance, created = await Email.objects.aget_or_create(
        message_id=email.message_id,
        defaults={
            SUBJECT: email.subject,
            MAIL_FROM: email.mail_from,
            DATE: email.date,
            RECEIVED: email.received,
            TEXT: email.text,
        },
    )
    if not created:
        email_instance.message_id = email.message_id
        email_instance.subject = email.subject
        email_instance.mail_from = email.mail_from
        email_instance.date = email.date
        email_instance.received = email.received
        email_instance.text = email.text
        await sync_to_async(email_instance.save)()
    attachments_with_url = []
    if attachments:
        for attachment in attachments:
            subfolder = generate_subfolder_name(email_instance.subject)
            safe_filename_max_length = (
                AttachmentConfig.ATTACHMENT_FILENAME_MAX_LENGTH
                - sum(
                    len(obj)
                    for obj in [
                        settings.ATTACHMENTS_URL,
                        email_account.email,
                        subfolder,
                    ]
                )
            )
            safe_filename = sanitize_and_truncate_filename(
                attachment[FILENAME], max_length=safe_filename_max_length
            )
            file_path = os.path.join(
                settings.ATTACHMENTS_URL,
                email_account.email,
                subfolder,
                safe_filename,
            )
            if not await sync_to_async(default_storage.exists)(file_path):
                content_file = ContentFile(attachment[CONTENT])
                await sync_to_async(default_storage.save)(
                    file_path, content_file
                )
            file_url = await sync_to_async(default_storage.url)(file_path)
            await sync_to_async(Attachment.objects.create)(
                email=email_instance,
                file=file_path,
                filename=safe_filename,
                url=file_url,
            )
            attachments_with_url.append(
                {FILENAME: safe_filename, URL: file_url}
            )
            save_email_to_db_logger.info(
                SAVE_EMAIL_ATTACHMENTS_TO_DB_SUCCESS,
                safe_filename,
                email.message_id,
            )
    save_email_to_db_logger.info(SAVE_EMAIL_TO_DB_SUCCESS, email.message_id)
    return email_instance, attachments_with_url
