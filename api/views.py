from nanoid import generate as generate_nanoid

from django.core.files.base import ContentFile
from django.urls import reverse
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status

from core.models import DocumentSigningRequest, SMS, Document
from .serializers import SendSMSSerializer
from .services import (
    create_document_from_html,
    generate_confirmation_code,
    send_document_signing_request,
)


# Create your views here.
class SendSMSView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = SendSMSSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            document_content = create_document_from_html(data["document"]["html"])
            if not document_content:
                return Response(
                    {"success": False, "error": "pdf file generating error"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            document_file = ContentFile(
                document_content, name=f"{generate_nanoid()}.pdf"
            )
            document = Document(file=document_file, name=data["document"]["name"])
            document.save()
            sms = SMS(phone_number=data["phone_number"], message="Hello")
            sms.save()
            signing_request = DocumentSigningRequest(
                document=document,
                phone_number=data["phone_number"],
                code=generate_confirmation_code(),
                sms=sms,
            )
            signing_request.save()
            send_document_signing_request(
                to=data["phone_number"],
                request_url=request.build_absolute_uri(
                    reverse("document", kwargs={"id": signing_request.id})
                ),
                request=signing_request,
            )
            print(
                request.build_absolute_uri(
                    reverse("document", kwargs={"id": signing_request.id})
                ),
                signing_request.code,
            )
            return Response({"success": True}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
