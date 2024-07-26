from django.urls import re_path
from mail_recipient import consumers

websocket_urlpatterns = [
    re_path(r'ws/email/$', consumers.EmailConsumer.as_asgi()),
]
