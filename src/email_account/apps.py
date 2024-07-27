from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Базовая конфигурация для приложения email_account.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "email_account"
    verbose_name = "Пользователи"
