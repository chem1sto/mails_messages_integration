import os
from django.core.exceptions import ValidationError


def validate_file_does_not_exist(value):
    file_path = value.path
    if os.path.exists(file_path):
        raise ValidationError(f"Файл {file_path} уже существует.")
