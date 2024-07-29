import os
from datetime import datetime
from email.message import Message
from typing import Any

from core.constants import (
    ATTACHMENTS_MAX_LENGTH,
    CONTENT,
    CONTENT_DISPOSITION,
    FILENAME,
    MULTIPART,
    SERIALIZE_DATETIME_ERROR_MESSAGE,
    TEXT_PLANE,
    TEXT_HTML,
)


def attachments_file_path(instance, filename: str) -> str | bytes:
    """Формирование пути и названия для загружаемого файла из вложений."""
    return os.path.join(instance.subject[:ATTACHMENTS_MAX_LENGTH], filename)


def get_attachments_from_message(message: Message) -> list[dict[str, Any]]:
    """Извлечение прикреплённых файлов из сообщения."""
    attachments = []
    for part in message.walk():
        if part.get_content_maintype() == MULTIPART:
            continue
        if part.get(CONTENT_DISPOSITION) is None:
            continue
        filename = part.get_filename()
        if filename:
            attachments.append(
                {
                    FILENAME: filename,
                    CONTENT: part.get_payload(decode=True),
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
