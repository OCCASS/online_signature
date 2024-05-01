from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files import File
from . import forms, service, models


@login_required
def index(request, *args, **kwargs):
    return render(request, "admin_panel/index.html")


@login_required
def create_document(request, *args, **kwargs):
    if request.method == "POST":
        form = forms.CreateDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("admin_panel_index")
    else:
        form = forms.CreateDocumentForm()

    return render(request, "admin_panel/create_document.html", context={"form": form})


@login_required
def documents(request, *args, **kwargs):
    documents_list = models.Document.objects.all().order_by("-created_at")
    return render(
        request, "admin_panel/documents.html", context={"documents": documents_list}
    )


@login_required
def create_document_signing_request(request, *args, **kwargs):
    if request.method == "POST":
        form = forms.CreateDocumentSigningRequestForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            confirmation_code = service.generate_confirmation_code()
            result = service.create_pdf_documnet(data["document_content"])
            if result.err:
                return HttpResponse(status=500)
            signing_request = models.DocumentSigningRequest(
                phone_number=data["phone_number"],
                confirmation_code=confirmation_code,
                document=data["document"],
                document_file=File(result.dest, name="document.pdf"),
                document_content=data["document_content"],
            )
            signing_request.save()
            sms = service.send_document_signing_sms(request, signing_request)
            signing_request.sms = sms
            signing_request.save()
            print(sms.message)
            return redirect("admin_panel_index")
    else:
        form = forms.CreateDocumentSigningRequestForm()

    return render(
        request,
        "admin_panel/create_document_signing_request.html",
        context={"form": form},
    )


def get_document(request, id: str, *args, **kwargs):
    document = get_object_or_404(models.Document, id=id)
    return JsonResponse(
        {
            "name": document.name,
            "template": document.template,
            "created_at": document.created_at,
        }
    )


@login_required
def edit_document(request, id, *args, **kwargs):
    document = get_object_or_404(models.Document, id=id)
    if request.method == "POST":
        form = forms.EditDocumentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            document.name = data["name"]
            document.template = data["template"]
            document.save()
            return redirect(request.path)
    else:
        form = forms.EditDocumentForm()

    return render(
        request,
        "admin_panel/edit_document.html",
        context={"document": document, "form": form},
    )


@login_required
def signed_documents(request, *args, **kwargs):
    signed_documents = models.DocumentSigningRequest.objects.filter(signed=True)
    return render(
        request,
        "admin_panel/signed_documents.html",
        context={"documents": signed_documents},
    )
