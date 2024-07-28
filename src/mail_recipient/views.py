from django.shortcuts import render
from .models import Email


def email_list(request):
    return render(request, "email_list.html")
