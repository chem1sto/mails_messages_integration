from django import forms
from .models import EmailAccount


class EmailAccountForm(forms.ModelForm):
    class Meta:
        model = EmailAccount
        fields = ["email", "password"]
        widgets = {
            "password": forms.PasswordInput(),
        }
