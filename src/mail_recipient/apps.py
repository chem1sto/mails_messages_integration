from django.apps import AppConfig


class MailRecipientConfig(AppConfig):
    """
    Базовая конфигурация для приложения mail_recipient.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mail_recipient'
    verbose_name = "Получатель почты"
