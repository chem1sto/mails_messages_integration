from django.db import models
from django.contrib.auth.models import User

from core.constants import EmailAccountConfig


class EmailAccount(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=EmailAccountConfig.USER_VERBOSE_NAME,
        help_text=EmailAccountConfig.USER_HELP_TEXT,
    )
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
