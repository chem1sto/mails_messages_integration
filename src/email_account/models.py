from django.db import models

from core.constants import EmailAccountConfig


class EmailAccount(models.Model):
    email = models.EmailField(
        verbose_name=EmailAccountConfig.EMAIL_VERBOSE_NAME,
        help_text=EmailAccountConfig.EMAIL_HELP_TEXT,
    )
    password = models.CharField(
        max_length=EmailAccountConfig.PASSWORD_MAX_LENGTH,
        verbose_name=EmailAccountConfig.PASSWORD_VERBOSE_NAME,
        help_text=EmailAccountConfig.PASSWORD_HELP_TEXT,
    )
