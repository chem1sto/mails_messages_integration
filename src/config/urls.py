"""
Конфигурация URL-адресов для проекта test_mails_message_integration.

URL-адреса:
- `admin/`: Административная панель Django.
- `""`: Главная страница, включает URL-адреса из приложения `email_account`.

Список `urlpatterns` направляет URL-адреса в представления.
Дополнительная информация об этом файле доступна по ссылке
    https://docs.djangoproject.com/en/stable/topics/http/urls/
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("email_account.urls")),
]
