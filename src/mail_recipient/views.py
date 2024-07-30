"""Представления для приложения Mail Recipient."""
import os

from django.conf import settings
from django.http import FileResponse, JsonResponse
from django.shortcuts import render

from core.constants import EMAIL_LIST_HTML, FILE_NOT_FOUND, FILENAME


def email_list(request):
    """
    Отображает страницу со списком электронных писем.

    Аргументы:
        request (HttpRequest): Объект запроса Django.

    Возвращает:
        HttpResponse: Ответ, содержащий HTML-страницу со списком электронных
    писем.
    """
    return render(request, EMAIL_LIST_HTML)


def download_file(request, filename):
    """
    Обрабатывает запрос на скачивание файла.

    Args:
        request (HttpRequest): Объект запроса Django.
        filename (str): Имя файла для скачивания.

    Returns:
        HttpResponse: Ответ, содержащий файл для скачивания или JSON-ответ с
    ошибкой, если файл не найден.
    """
    file_path = os.path.join(settings.ATTACHMENTS_ROOT, filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, "rb"), as_attachment=True)
    else:
        return JsonResponse({FILE_NOT_FOUND: True, FILENAME: filename})
