from django import forms
from django.contrib.auth.forms import AuthenticationForm
from . import models, fields


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Логин"}),
        help_text="Данные для входа можно получить у админа системы",
    )
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}),
        help_text="Данные для входа можно получить у админа системы",
    )


class CreateDocumentForm(forms.ModelForm):
    class Meta:
        model = models.Document
        fields = ["name", "template"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Название документа"}),
            "template": forms.Textarea(attrs={"placeholder": "Шаблон документа"}),
        }
        labels = {"name": "", "template": ""}
        help_texts = {
            "name": "Название документа для удобного поиска",
            "template": "Шаблон документа, при создании документа в шаблон можно будет добавить персональную информацию пользователя",
        }


class CreateDocumentSigningRequestForm(forms.Form):
    phone_number = fields.PhoneNumberField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Номер телефона", "type": "tel"}),
        help_text="Номер телефона клиента начиная с 8",
    )
    document = forms.ModelChoiceField(
        models.Document.objects.all().order_by("created_at"),
        label="",
        help_text="Документ для подписи",
    )
    document_content = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={"placeholder": "Содержание документа", "hidden": "hidden"}
        ),
        required=False,
    )


class EditDocumentForm(forms.Form):
    name = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": "Название документа"})
    )
    template = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={"placeholder": "Шаблон документа"}),
        help_text="Измените содержание документа",
    )
