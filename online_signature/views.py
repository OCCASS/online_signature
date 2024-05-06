from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.utils import timezone

from core.models import DocumentSigningRequest
from .forms import SignDocumentForm
from .services import sign_document

# Create your views here.
def index_view(request, *args, **kwargs):
    return render(request, "index.html")


def document_view(request, id, *args, **kwargs):
    signing_request = get_object_or_404(DocumentSigningRequest, id=id)

    if signing_request.signed:
        return render(request, "document.html", {"document": signing_request})
    elif signing_request.expires_at < timezone.now():
        return render(request, "document_signing_expired.html")
    elif signing_request.attempts == settings.DOCUMENT_SIGNING_REQUEST_MAX_ATTEMPTS:
        return render(request, "document_signing_max_attempts_count.html")

    if request.method == "POST":
        form = SignDocumentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if signing_request.code == data["confirmation_code"]:
                signing_request.sign()
                sign_document(signing_request)
                return render(
                    request,
                    "document.html",
                    {
                        "document": signing_request,
                    },
                )
            else:
                signing_request.attempts += 1
                signing_request.save()
                form.add_error("confirmation_code", "Введен неверный код")
    else:
        form = SignDocumentForm()

    return render(
        request,
        "document.html",
        {
            "document": signing_request,
            "form": form,
        },
    )
