import os
from email.message import Message
from typing import Any


def email_file_path(instance, filename: str) -> str:
    """Формирование пути загрузки файла, включая оригинальное название."""
    return os.path.join("email_files", instance.subject[:50], filename)


def get_text_from_message(message: Message) -> str:
    """Извлечение текста из сообщения."""
    text = ""
    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                text += part.get_payload(decode=True).decode()
            elif content_type == "text/html":
                text += part.get_payload(decode=True).decode()
    else:
        text = message.get_payload(decode=True).decode()
    return text


def get_attachments_from_message(message: Message) -> list[dict[str, Any]]:
    """Извлечение прикреплённых файлов из сообщения."""
    attachments = []
    for part in message.walk():
        if part.get_content_maintype() == "multipart":
            continue
        if part.get("Content-Disposition") is None:
            continue
        filename = part.get_filename()
        if filename:
            attachments.append(
                {
                    "filename": filename,
                    "content": part.get_payload(decode=True),
                }
            )
    return attachments
