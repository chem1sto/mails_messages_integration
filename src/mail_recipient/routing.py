from django.urls import re_path
from mail_recipient.consumers import EmailListConsumer

websocket_urlpatterns = [
    re_path(r"ws/email_list/$", EmailListConsumer.as_asgi()),
]
