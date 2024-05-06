from django.db import models
from django.utils import timezone
from django.conf import settings
from nanoid import generate as generate_nanoid
from functools import partial


class Document(models.Model):
    """Модель загруженного документа"""

    class Meta:
        db_table = "document"

    id = models.CharField(
        default=partial(generate_nanoid, size=12), primary_key=True, max_length=12
    )
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="documents/")


class SMS(models.Model):
    """Модель отправленного СМС"""

    class Meta:
        db_table = "sms"

    id = models.CharField(
        default=partial(generate_nanoid, size=12), primary_key=True, max_length=12
    )
    phone_number = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    resend_at = models.DateTimeField(null=True)
    can_resend_at = models.DateTimeField(null=True)
    can_resend = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.can_resend_at = (
            timezone.now() + settings.DOCUMENT_SIGNING_REQUEST_RESEND_SMS_DELAY
        )
        return super().save(*args, **kwargs)


class DocumentSigningRequest(models.Model):
    """Модель запроса на подписание документа"""

    class Meta:
        db_table = "document_signing_request"

    id = models.CharField(
        default=partial(generate_nanoid, size=12), primary_key=True, max_length=12
    )
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    code = models.CharField(max_length=4)
    sms = models.ForeignKey(SMS, on_delete=models.CASCADE)
    attempts = models.IntegerField(default=0)
    signed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True)
    signed_at = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.expires_at = timezone.now() + settings.DOCUMENT_SIGNING_REQUEST_LIFETIME
        return super().save(*args, **kwargs)

    def sign(self, *args, **kwargs):
        self.signed = True
        self.signed_at = timezone.now()
        super().save()
