import re

from django import forms
from django.core.exceptions import ValidationError


class PhoneNumberField(forms.Field):
    def validate(self, value):
        super().validate(value)
        self._validate_phone_number(value)

    def _validate_phone_number(self, value):
        valid = bool(
            re.match(
                r"^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$",
                value,
            )
        )
        if not valid:
            raise ValidationError("Не корректный номер телефона")
