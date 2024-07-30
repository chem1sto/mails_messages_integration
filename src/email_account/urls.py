"""
Конфигурация URL-адресов для приложений email_account и mail_recipient.

Список `urlpatterns` направляет URL-адреса в представления.

URL-адреса:
- `""`: Главная страница, отображает форму для добавления email-аккаунта.
- `"email_list/"`: Страница со списком email-сообщений.
- `"attachments/(?P<filename>.*)$"`: Маршрут для скачивания вложений, где
`filename` - имя файла вложения.

Дополнительная информация об этом файле доступна по ссылке
    https://docs.djangoproject.com/en/stable/topics/http/urls/
"""

from django.urls import path, re_path

from email_account.views import add_email_account
from mail_recipient.views import download_file, email_list

urlpatterns = [
    path("", add_email_account, name="add_email_account"),
    path("email_list/", email_list, name="email_list"),
    re_path(
        r"^attachments/(?P<filename>.*)$", download_file, name="download_file"
    ),
]
