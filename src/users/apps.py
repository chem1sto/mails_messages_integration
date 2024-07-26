from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Базовая конфигурация для приложения users.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = "Пользователи"
