import os

from django.conf import settings
from django.http import FileResponse, HttpResponseNotFound
from django.shortcuts import render

from core.constants import EMAIL_LIST_HTML, FILE_NOT_FOUND


def email_list(request):
    return render(request, EMAIL_LIST_HTML)


def download_file(request, filename):
    file_path = os.path.join(settings.ATTACHMENTS_ROOT, filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, "rb"), as_attachment=True)
    else:
        return HttpResponseNotFound(FILE_NOT_FOUND)
