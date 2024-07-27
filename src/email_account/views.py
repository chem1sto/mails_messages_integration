from django.shortcuts import render, redirect
from email_account.forms import EmailAccountForm
from email_account.models import EmailAccount
from django.contrib.auth.hashers import make_password


def add_email_account(request):
    if request.method == "POST":
        form = EmailAccountForm(request.POST)
        if form.is_valid():
            email_account = form.save(commit=False)
            email_account.password = make_password(form.cleaned_data['password'])
            email_account.save()
            return redirect("email_list")
    else:
        form = EmailAccountForm()
    return render(request, "add_email_account.html", {"form": form})
