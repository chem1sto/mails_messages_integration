"""
ASGI конфиг для проекта test_mails_message_integration.

Он предоставляет вызываемый ASGI как переменную уровня модуля с именем
 «application».

Дополнительная информация об этом файле доступна по ссылке
https://docs.djangoproject.com/en/stable/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from mail_recipient import routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(routing.websocket_urlpatterns)
        ),
    }
)
