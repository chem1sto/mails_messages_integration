"""Валидаторы для модели Email."""
import os

from django.core.exceptions import ValidationError


def validate_file_does_not_exist(value):
    """
    Валидатор, который проверяет, что файл не существует по указанному пути.

    Аргументы:
        value (str): Путь к файлу.

    Вызывает ошибку:
        ValidationError: Если файл по указанному пути уже существует.
    """
    file_path = value.path
    if os.path.exists(file_path):
        raise ValidationError(f"Файл {file_path} уже существует.")
