from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files import File
from . import forms
from core.models import DocumentSigningRequest, Document


@login_required
def index(request, *args, **kwargs):
    return render(request, "admin_panel/index.html")


@login_required
def signed_documents(request, *args, **kwargs):
    signed_documents = DocumentSigningRequest.objects.all().order_by("-created_at")
    return render(
        request,
        "admin_panel/signed_documents.html",
        context={"documents": signed_documents},
    )
