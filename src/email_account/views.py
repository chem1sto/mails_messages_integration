from django.shortcuts import render, redirect

from email_account.forms import EmailAccountForm
from email_account.models import EmailAccount

from core.constants import (
    ADD_EMAIL_ACCOUNT_HTML,
    EMAIL,
    EMAIL_LIST_REDIRECT,
    FORM,
    PASSWORD,
    REQUEST_METHOD,
)


def add_email_account(request):
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
