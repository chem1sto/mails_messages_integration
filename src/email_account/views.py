from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect

from email_account.forms import EmailAccountForm
from email_account.models import EmailAccount


def add_email_account(request):
    if request.method == "POST":
        form = EmailAccountForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            email_account, created = EmailAccount.objects.get_or_create(
                email=email)
            email_account.password = make_password(password)
            email_account.save()
            return redirect(f"/email_list/?email={email}")
    else:
        form = EmailAccountForm()
    return render(request, "add_email_account.html", {"form": form})
