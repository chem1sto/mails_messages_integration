from django.shortcuts import render
from .models import Email


def email_list(request):
    emails = Email.objects.filter(user=request.user)
    return render(request, 'email_list.html', {'emails': emails})
