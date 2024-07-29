from django.urls import path, re_path

from email_account.views import add_email_account
from mail_recipient.views import email_list, download_file

urlpatterns = [
    path("", add_email_account, name="add_email_account"),
    path("email_list/", email_list, name="email_list"),
    re_path(
        r"^attachments/(?P<path>.*)$", download_file, name="download_file"
    ),
]
