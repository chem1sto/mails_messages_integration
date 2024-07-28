from django.db import models

from core.constants import EmailAccountConfig
from django.db.models import UniqueConstraint


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

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=[EmailAccountConfig.EMAIL, EmailAccountConfig.PASSWORD],
                name=EmailAccountConfig.UNIQUE_EMAIL_PASSWORD_NAME)
        ]
