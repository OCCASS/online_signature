from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from admin_panel.models import DocumentSigningRequest
from .forms import SignDocumentForm
from . import services

# Create your views here.
def index_view(request, *args, **kwargs):
    return render(request, "index.html")


def document_view(request, id, *args, **kwargs):
    document_signing_request = get_object_or_404(DocumentSigningRequest, id=id)

    if document_signing_request.signed:
        return render(request, "document.html", {"document": document_signing_request})
    elif document_signing_request.expires_at < timezone.now():
        return render(request, "document_signing_expired.html")
    elif document_signing_request.attempts == 3:
        return render(request, "document_signing_max_attempts_count.html")

    if request.method == "POST":
        form = SignDocumentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if document_signing_request.confirmation_code == data["confirmation_code"]:
                document_signing_request.sign()
                services.generate_signed_document(document_signing_request)
                return render(
                    request,
                    "document.html",
                    {
                        "document": document_signing_request,
                    },
                )
            else:
                document_signing_request.attempts += 1
                document_signing_request.save()
                form.add_error("confirmation_code", "Введен неверный код")
    else:
        form = SignDocumentForm()

    return render(
        request,
        "document.html",
        {
            "document": document_signing_request,
            "form": form,
        },
    )
