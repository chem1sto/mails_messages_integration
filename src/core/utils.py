import os


def email_file_path(instance, filename):
    """Формирование пути загрузки файла, включая оригинальное название."""
    return os.path.join("email_files", instance.subject[:50], filename)
