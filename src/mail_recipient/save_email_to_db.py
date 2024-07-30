"""Модуль save_email_to_db."""
import logging

from asgiref.sync import sync_to_async
from django.core.files.base import ContentFile

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
)
from mail_recipient.models import Email

save_email_to_db_logger = logging.getLogger(SAVE_EMAIL_TO_DB)


async def save_email_to_db(email: Email, attachments: list):
    """Сохранение электронного письма в БД."""
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
        await sync_to_async(email_instance.save)(
            force_insert=False,
            force_update=True,
            using=None,
            update_fields=None,
        )
    save_email_to_db_logger.info(SAVE_EMAIL_TO_DB_SUCCESS, email.message_id)
    for attachment in attachments:
        filename = attachment[FILENAME]
        content = attachment[CONTENT]
        content_file = ContentFile(content)
        await sync_to_async(email_instance.attachments.save)(
            filename, content_file
        )
        save_email_to_db_logger.info(
            SAVE_EMAIL_ATTACHMENTS_TO_DB_SUCCESS,
            filename,
            email.message_id,
        )
