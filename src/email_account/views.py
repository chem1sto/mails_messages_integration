from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect

from email_account.forms import EmailAccountForm
from email_account.models import EmailAccount


def add_email_account(request):
    if request.method == "POST":
        form = EmailAccountForm(request.POST)
        if form.is_valid():
            if EmailAccount.objects.filter(
                    email=form.cleaned_data["email"]).first():
                return redirect("email_list")
            else:
                email_account = form.save(commit=False)
                email_account.password = make_password(
                    form.cleaned_data["password"]
                )
                email_account.save()
                return redirect("email_list")
    else:
        form = EmailAccountForm()
    return render(request, "add_email_account.html", {"form": form})
