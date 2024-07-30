import os
import re

from core.constants import (
    ATTACHMENTS,
    ATTACHMENTS_MAX_LENGTH,
    SRC,
)


def format_file_or_folder_path(object_name: str) -> str:
    """Формирование названий файлов и папок с разрешёнными в url символами."""
    forbidden_chars = r" <>\"\'#%{}|\\^~[]`"
    for char in forbidden_chars:
        object_name = object_name.replace(char, "_")
    object_name = re.sub(r"_+", "_", object_name)
    return object_name


def format_attachments_file_path(subject: str, filename: str) -> str | bytes:
    """Формирование пути и названия для загружаемого файла из вложений."""
    return os.path.join(
        SRC,
        ATTACHMENTS,
        format_file_or_folder_path(subject[:ATTACHMENTS_MAX_LENGTH]),
        format_file_or_folder_path(filename),
    )
