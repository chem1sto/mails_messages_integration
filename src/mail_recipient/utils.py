from os import remove

from asgiref.sync import sync_to_async
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from core.constants import CONTENT, FILENAME
from mail_recipient.models import Email


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
        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(content)
            temp_file.flush()
            with open(temp_file.name, "rb") as f:
                await sync_to_async(email.attachments.save)(filename, File(f))
        remove(temp_file.name)
