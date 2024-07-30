"""Представления для приложения email_account."""

from django.shortcuts import redirect, render

from core.constants import (
    ADD_EMAIL_ACCOUNT_HTML,
    EMAIL,
    EMAIL_LIST_REDIRECT,
    FORM,
    PASSWORD,
    REQUEST_METHOD,
)
from email_account.forms import EmailAccountForm
from email_account.models import EmailAccount


def add_email_account(request):
    """
    Представление для добавления или обновления учетной записи email.

    Это представление обрабатывает запросы на добавление или обновление
    учетной записи email.
    Если запрос является POST, оно проверяет форму и сохраняет учетную запись.
    Если учетная запись уже существует, она обновляет пароль.
    Если запрос не является POST, оно отображает пустую форму.

    Аргументы:
        request (HttpRequest): Объект запроса Django.

    Возвращает:
        HttpResponse: Ответ, содержащий HTML-страницу с формой или
    перенаправление на список email-сообщений.

    Вызывает ошибку:
        Exception: Если возникает ошибка при сохранении учетной записи.
    """
    if request.method == REQUEST_METHOD:
        form = EmailAccountForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data[EMAIL]
            password = form.cleaned_data[PASSWORD]
            try:
                email_account, created = EmailAccount.objects.get_or_create(
                    email=email, defaults={PASSWORD: password}
                )
                if not created:
                    email_account.password = password
                    email_account.save()
                return redirect(EMAIL_LIST_REDIRECT.format(email=email))
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = EmailAccountForm()
    return render(request, ADD_EMAIL_ACCOUNT_HTML, {FORM: form})
