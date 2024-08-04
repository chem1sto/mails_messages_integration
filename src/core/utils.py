"""Функции для получения корректных данных из электронных писем."""

import hashlib
from email.message import Message
from typing import Any

import chardet
from bs4 import BeautifulSoup

from core.constants import (
    BS4_PARSER,
    CONTENT,
    CONTENT_DISPOSITION,
    ENCODING,
    FILENAME,
    HASHED_SUBJECT_MAX_LENGTH,
    MULTIPART,
    TEXT_HTML,
    TEXT_PLANE,
)


def add_text_from_part(str_obj: str, part: Message = None) -> str:
    """
    Получение текста из части сообщения и добавление его к существующей строке.

    Аргументы:
        str_obj (str): Строка, к которой будет добавлен извлеченный текст.
        part (email.message.Message, optional): Часть сообщения, из которой
    нужно извлечь текст.

    Возвращает:
        str: Строка с добавленным извлеченным текстом.
    """
    str_obj += decode_text(part.get_payload(decode=True))
    return str_obj


def cast_redis_hosts(value: str) -> tuple:
    """
    Преобразует строку в кортеж, содержащий хост и порт Redis.

    Аргументы:
    - value (str): Строка, содержащая хост и порт, разделенные запятой и
    пробелом.

    Возвращает:
    - tuple: Кортеж, содержащий хост (str) и порт (int).
    """
    host, port = value.split(", ")
    return tuple([host, int(port)])


def decode_text(payload: bytes) -> str:
    """
    Декодирует текст с автоматическим определением кодировки.

    Аргументы:
        payload (bytes): Байтовый массив текста.

    Возвращает:
        str: Декодированный текст.
    """
    try:
        return payload.decode()
    except UnicodeDecodeError:
        return payload.decode(chardet.detect(payload)[ENCODING])


def get_attachments_from_message(message: Message) -> list[dict[str, Any]]:
    """
    Извлечение прикреплённых файлов из сообщения.

    Аргументы:
        message (Message): Объект сообщения электронной почты.

    Возвращает:
        List[Dict[str, Any]]: Список словарей, каждый из которых содержит
        информацию о прикреплённом файле.
            Каждый словарь содержит следующие ключи:
            - 'filename' (str): Имя файла.
            - 'content' (bytes): Содержимое файла в виде байтового массива.
    """
    attachments = []
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
                }
            )
    return attachments


def extract_text_from_message(message: Message) -> str:
    """
    Извлечение текста из сообщения.

    Аргументы:
        message (Message): Объект сообщения электронной почты.

    Возвращает:
        str: Строка, содержащая извлеченный текст из сообщения.
    """
    text = ""
    html = ""
    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            if content_type == TEXT_PLANE:
                text += add_text_from_part(text, part)
            elif content_type == TEXT_HTML:
                html += add_text_from_part(text, part)
    else:
        content_type = message.get_content_type()
        if content_type == TEXT_PLANE:
            text += add_text_from_part(text, message)
        elif content_type == TEXT_HTML:
            html += add_text_from_part(text, message)
    if html:
        soup = BeautifulSoup(html, BS4_PARSER)
        text += soup.get_text()
    return " ".join(text.strip().split())


def sanitize_and_truncate_filename(filename: str, max_length: int) -> str:
    """
    Создание имени файла, не превышающего заданную максимальную длину.

    Аргументы:
        filename (str): Исходное имя файла.
        max_length (int): Максимальная длина имени файла.

    Возвращает:
        str: Очищенное и усеченное имя файла.
    """
    sanitized_filename = "".join(
        c for c in filename if c.isalnum() or c in " .-_"
    )
    return sanitized_filename[:max_length]


def generate_subfolder_name(subject: str) -> str:
    """
    Создание хэшированного имени подпапки на основе темы письма.

    Аргументы:
        subject (str): Тема письма.

    Возвращает:
        str: Хэшированное имя подпапки.
    """
    hashed_subject = hashlib.sha256(subject.encode()).hexdigest()[
        :HASHED_SUBJECT_MAX_LENGTH
    ]
    return hashed_subject
