from django import forms
from django.conf import settings


class SignDocumentForm(forms.Form):
    confirmation_code = forms.CharField(
        label="",
        max_length=settings.CONFIRMATION_CODE_LENGTH,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Код из СМС",
                "class": "form__input",
                "type": "tel",
            }
        ),
    )
