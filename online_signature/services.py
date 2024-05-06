import os
import io
import requests

from django.conf import settings
from typing import Optional
from django.core.files import File
from core.models import DocumentSigningRequest


def _get_signed_document(file: bytes, phone_number: str, code: str) -> Optional[bytes]:
    url = settings.PDF_MAKER_HOST + "/sign"
    response = requests.post(
        url, data={"phoneNumber": phone_number, "code": code}, files={"file": file}
    )
    if response.status_code == 201:
        return response.content
    return None


def sign_document(sign_request: DocumentSigningRequest) -> None:
    signed_document_bytes = _get_signed_document(
        sign_request.document.file.file,
        sign_request.phone_number,
        sign_request.code,
    )
    if signed_document_bytes:
        document = sign_request.document
        new_file = File(
            io.BytesIO(signed_document_bytes),
            name=os.path.basename(document.file.name),
        )
        document.file.delete()
        document.file = new_file
        document.save()
