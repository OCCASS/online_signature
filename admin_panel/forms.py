from django import forms
from django.contrib.auth.forms import AuthenticationForm


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
