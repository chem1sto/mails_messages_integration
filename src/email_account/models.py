from django.contrib.auth.hashers import make_password, check_password
from django.db import models

from core.constants import EmailAccountConfig


class EmailAccount(models.Model):
    email = models.EmailField(
        unique=True,
        verbose_name=EmailAccountConfig.EMAIL_VERBOSE_NAME,
        help_text=EmailAccountConfig.EMAIL_HELP_TEXT,
    )
    password = models.CharField(
        max_length=128,
        verbose_name=EmailAccountConfig.PASSWORD_VERBOSE_NAME,
        help_text=EmailAccountConfig.PASSWORD_HELP_TEXT,
    )
