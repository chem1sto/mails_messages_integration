from django.shortcuts import render, redirect
from .forms import EmailAccountForm


def add_email_account(request):
    if request.method == "POST":
        form = EmailAccountForm(request.POST)
        if form.is_valid():
            email_account = form.save(commit=False)
            email_account.user = request.user
            email_account.save()
            return redirect("email_list")
    else:
        form = EmailAccountForm()
    return render(request, "add_email_account.html", {"form": form})
