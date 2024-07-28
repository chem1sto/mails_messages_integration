from django.shortcuts import render


def email_list(request):
    return render(request, "email_list.html")
