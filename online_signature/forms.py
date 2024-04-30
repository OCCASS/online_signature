from django import forms
from django.conf import settings


class SignDocumentForm(forms.Form):
    class Media:
        js = ["js/confirmation_code_again_counter.js"]

    confirmation_code = forms.CharField(
        max_length=settings.CONFIRMATION_CODE_LENGTH,
        widget=forms.TextInput(
            attrs={"placeholder": "Код из СМС", "class": "form__input"}
        ),
    )
