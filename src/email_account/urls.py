from django.urls import path

from email_account.views import add_email_account
from mail_recipient.views import email_list

urlpatterns = [
    path("", add_email_account, name="add_email_account"),
    path("email_list/", email_list, name="email_list"),
]
