import random
import requests
import string

from django.conf import settings
from django_twilio.client import twilio_client
from typing import Optional
from core.models import DocumentSigningRequest


def create_document_from_html(html: str) -> Optional[bytes]:
    url = settings.PDF_MAKER_HOST + "/make"
    response = requests.post(url, json={"html": html})
    if response.status_code == 201:
        return response.content
    return None


def generate_confirmation_code() -> str:
    code = ""
    numbers = string.digits
    for i in range(settings.CONFIRMATION_CODE_LENGTH):
        code += random.choice(numbers.replace("0", "") if i == 0 else numbers)
    return code


def send_document_signing_request(
    *, to: str, request_url: str, request: DocumentSigningRequest
) -> None:
    message = (
        "Здравсвуйте, это Ваша ссылка на подписание документа: %s\nВаш код подтверждения: *%s*"
        % (
            request_url,
            request.code,
        )
    )
    send_sms(to, message)


def send_sms(to: str, message: str) -> None:
    # TODO: add status code return
    twilio_client.messages.create(
        from_="whatsapp:+14155238886",
        to=f"whatsapp:{to}",
        body=message,
    )
