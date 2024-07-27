from django.contrib import admin
from django.urls import path

from mail_recipient.views import email_list
from email_account.views import add_email_account

urlpatterns = [
    path("", add_email_account, name="add_email_account"),
    path("mail_recipient/", email_list, name="email_list")
]
