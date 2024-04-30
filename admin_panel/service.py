import string
import random

from django.conf import settings
from django.urls import reverse
from xhtml2pdf import pisa
from io import BytesIO
from .models import DocumentSigningRequest, SMS


def generate_confirmation_code() -> str:
    code = ""
    numbers = string.digits
    for i in range(settings.CONFIRMATION_CODE_LENGTH):
        code += random.choice(numbers.replace("0", "") if i == 0 else numbers)
    return code


def send_document_signing_sms(
    request, document_signing_request: DocumentSigningRequest
) -> SMS:
    url = reverse("document", kwargs={"id": document_signing_request.id})
    absolute_url = request.build_absolute_uri(url)
    message = (
        "Hello, this is your document to sign: %s. Your confirmation code is: %s"
        % (
            absolute_url,
            document_signing_request.confirmation_code,
        )
    )
    sms = SMS(
        message=message,
        status_code=0,
        phone_number=document_signing_request.phone_number,
    )
    sms.save()
    return sms


def create_pdf_documnet(content):
    html = """<html>
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type">
        <style>
            @page {
                size: A4;
                margin: 1cm;
                padding: 1cm;
            }

            @font-face {
                font-family: 'Times New Roman';
                src: url("static/fonts/times_new_roman.ttf"); 
            }

            body {
                font-size: 12pt;
                font-family: 'Times New Roman';
            }
          </style>
    </head>
    <body>%s</body>
    </html>""" % content.replace(
        "\n\r", "<br>"
    )
    result = pisa.CreatePDF(html, dest=BytesIO(), encoding="utf-8")
    return result
