"""Модуль save_email."""

import logging
from typing import Any

from asgiref.sync import sync_to_async
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from core.constants import (
    ATTACHMENT_FILE_PATH,
    ATTACHMENT_URL_PATH,
    ATTACHMENTS,
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
)
from mail_recipient.models import Attachment, Email

save_email_to_db_logger = logging.getLogger(SAVE_EMAIL_TO_DB)


async def save_email(
    email: Email, attachments: list, host: str, port: str
) -> tuple[Any, list]:
    """Сохранение электронного письма в БД и на локальном диске."""
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
            filename = attachment[FILENAME]
            content = attachment[CONTENT]
            content_file = ContentFile(content)
            file_path = ATTACHMENT_FILE_PATH.format(
                subfolder=email_instance.subject, filename=filename
            )
            await sync_to_async(default_storage.save)(file_path, content_file)
            file_url = await sync_to_async(default_storage.url)(file_path)
            await sync_to_async(Attachment.objects.create)(
                email=email_instance,
                file=file_path,
                filename=filename,
                url=file_url,
            )
            attachments_with_url.append(
                {
                    FILENAME: filename,
                    URL: ATTACHMENT_URL_PATH.format(
                        host=host,
                        port=port,
                        filename=file_path.split(ATTACHMENTS)[1],
                    ),
                }
            )
            save_email_to_db_logger.info(
                SAVE_EMAIL_ATTACHMENTS_TO_DB_SUCCESS,
                filename,
                email.message_id,
            )
    save_email_to_db_logger.info(SAVE_EMAIL_TO_DB_SUCCESS, email.message_id)
    return email_instance, attachments_with_url
