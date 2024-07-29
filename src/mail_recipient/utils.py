from os import remove

from asgiref.sync import sync_to_async
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from core.constants import CONTENT, FILENAME
from mail_recipient.models import Email


async def save_email_to_db(email: Email, attachments: list):
    """Сохранение электронного письма в БД."""
    email_instance, created = await Email.objects.aget_or_create(
        message_id=email.message_id,
        defaults={
            "subject": email.subject,
            "mail_from": email.mail_from,
            "date": email.date,
            "received": email.received,
            "text": email.text,
        }
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
    for attachment in attachments:
        filename = attachment[FILENAME]
        content = attachment[CONTENT]
        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(content)
            temp_file.flush()
            with open(temp_file.name, "rb") as f:
                await sync_to_async(email_instance.attachments.save)(
                    filename, File(f)
                )
        remove(temp_file.name)
