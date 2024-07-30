"""Функции для форматирования путей и названий файлов."""

import os
import re

from core.constants import (
    ATTACHMENTS,
    ATTACHMENTS_MAX_LENGTH,
    FORBIDDEN_CHARS,
    SRC,
)


def format_file_or_folder_path(object_name: str) -> str | None:
    """Формирование названий файлов и папок с разрешёнными в url символами."""
    if object_name is None:
        return object_name
    if not isinstance(object_name, str):
        object_name = str(object_name)
    for char in FORBIDDEN_CHARS:
        object_name = object_name.replace(char, "_")
    object_name = re.sub(r"_+", "_", object_name)
    return object_name


def format_attachments_file_path(subject: str, filename: str) -> str | bytes:
    """Формирование пути и названия для загружаемого файла из вложений."""
    full_path = os.path.join(
        SRC,
        ATTACHMENTS,
        format_file_or_folder_path(subject),
        format_file_or_folder_path(filename),
    )
    if len(full_path) > ATTACHMENTS_MAX_LENGTH:
        subject = subject[
            : ATTACHMENTS_MAX_LENGTH
            - len(SRC)
            - len(ATTACHMENTS)
            - len(filename)
            - 2
        ]
        full_path = os.path.join(SRC, ATTACHMENTS, subject, filename)
    return full_path
