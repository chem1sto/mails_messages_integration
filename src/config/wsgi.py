"""
WSGI конфиг для проекта test_mails_message_integration.

Он предоставляет вызываемый WSGI как переменную уровня модуля с именем
 «application».

Дополнительная информация об этом файле доступна по ссылке
https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
