"""Форма для ввода email и пароля."""
from django import forms
from django.core.validators import MinLengthValidator

from core.constants import EMAIL, PASSWORD, EmailAccountFormConfig
from email_account.models import EmailAccount


class EmailAccountForm(forms.ModelForm):
    """
    Форма для ввода email и пароля.

    Атрибуты:
        email (str): Email пользователя.
        password (str): Пароль пользователя.

    """

    password = forms.CharField(
        label=EmailAccountFormConfig.PASSWORD_LABEL,
        widget=forms.PasswordInput(),
        help_text=EmailAccountFormConfig.PASSWORD_HELP_TEXT,
        validators=[
            MinLengthValidator(
                8,
                message=EmailAccountFormConfig.PASSWORD_VALIDATOR_MESSAGE,
            )
        ],
    )

    class Meta:
        """Мета-класс для настройки формы EmailAccountForm."""

        model = EmailAccount
        fields = [EMAIL, PASSWORD]
        widgets = {
            PASSWORD: forms.PasswordInput(),
        }
