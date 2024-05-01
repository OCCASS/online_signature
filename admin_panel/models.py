from django.db import models
from django.utils import timezone
from django.conf import settings
from functools import partial
from nanoid import generate
from . import utils

import uuid


# Create your models here.
class SMS(models.Model):
    class Meta:
        db_table = "sms"

    id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=20, null=False)
    message = models.CharField(max_length=255)
    status_code = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class Document(models.Model):
    class Meta:
        db_table = "document"

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=255, null=False)
    template = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DocumentSigningRequest(models.Model):
    class Meta:
        db_table = "document_signing_request"

    id = models.CharField(
        default=partial(generate, size=12),
        primary_key=True,
    )
    phone_number = models.CharField(max_length=20)
    confirmation_code = models.CharField(max_length=8)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    document_file = models.FileField(upload_to="documents/")
    document_content = models.TextField()
    sms = models.ForeignKey(SMS, on_delete=models.CASCADE, null=True, blank=True)
    signed = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    signed_at = models.DateTimeField(null=True)
    expires_at = models.DateTimeField(null=True)
    resend_sms_from = models.DateTimeField(null=True)
    can_resend_sms = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.expires_at = timezone.now() + settings.DOCUMENT_SIGNING_REQUEST_LIFETIME
        self.resend_sms_from = (
            timezone.now() + settings.DOCUMENT_SIGNING_REQUEST_RESEND_SMS_DELAY
        )
        return super().save(*args, **kwargs)

    def sign(self):
        self.signed = True
        self.signed_at = timezone.now()
        super().save()

    @property
    def formatted_phone_number(self) -> str:
        return utils.format_phone_number(self.phone_number)
