from mail_recipient.models import Email
from django.core.files import File
from core.constants import (
    CONTENT,
    FILENAME,
)
from core.utils import attachments_file_path
from asgiref.sync import sync_to_async


async def save_email_to_db(email: Email, attachments: list):
    """Сохранение электронного письма в БД."""
    await sync_to_async(email.save)(
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    )
    for attachment in attachments:
        filename = attachment[FILENAME]
        content = attachment[CONTENT]
        with open(attachments_file_path(email, filename), "wb") as f:
            f.write(content)
        await sync_to_async(email.attachments.save)(filename, File(f))
