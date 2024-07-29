import os
from datetime import datetime
from email.message import Message
from typing import Any

from core.constants import (
    ATTACHMENTS,
    ATTACHMENT_PATH,
    ATTACHMENTS_MAX_LENGTH,
    CONTENT,
    CONTENT_DISPOSITION,
    FILENAME,
    MULTIPART,
    SERIALIZE_DATETIME_ERROR_MESSAGE,
    SRC,
    SUBJECT,
    TEXT_PLANE,
    TEXT_HTML,
    URL,
)


def attachments_file_path(instance, filename: str) -> str | bytes:
    """Формирование пути и названия для загружаемого файла из вложений."""
    return os.path.normpath(
        os.path.join(
            SRC,
            ATTACHMENTS,
            instance.subject[:ATTACHMENTS_MAX_LENGTH],
            filename,
        )
    )


def get_attachments_from_message(
    message: Message, host: str, port: str
) -> list[dict[str, Any]]:
    """Извлечение прикреплённых файлов из сообщения."""
    attachments = []
    subfolder = message[SUBJECT].replace(" ", "_").replace("/", "_")
    for part in message.walk():
        if part.get_content_maintype() == MULTIPART:
            continue
        if part.get(CONTENT_DISPOSITION) is None:
            continue
        filename = part.get_filename()
        if filename:
            content = part.get_payload(decode=True)
            attachments.append(
                {
                    FILENAME: filename,
                    CONTENT: content,
                    URL: ATTACHMENT_PATH.format(
                        host=host,
                        port=port,
                        subfolder=subfolder,
                        filename=filename,
                    ),
                }
            )
    return attachments


def get_text_from_message(message: Message) -> str:
    """Извлечение текста из сообщения."""
    text = ""
    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            if content_type == TEXT_PLANE:
                text += part.get_payload(decode=True).decode()
            elif content_type == TEXT_HTML:
                text += part.get_payload(decode=True).decode()
    else:
        text = message.get_payload(decode=True).decode()
    return text


def serialize_datetime(obj: datetime) -> str:
    """Сериализация объектов datetime в строки формата ISO."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(SERIALIZE_DATETIME_ERROR_MESSAGE)
