from django.urls import path
from . import views
from . import auth_views


urlpatterns = [
    path("", views.index, name="admin_panel_index"),
    path("login/", auth_views.LoginView.as_view(), name="admin_panel_login"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="admin_panel_logout",
    ),
    path("create_document/", views.create_document, name="admin_panel_create_document"),
    path("documents/", views.documents, name="admin_panel_documents"),
    path(
        "create_document_signing_request/",
        views.create_document_signing_request,
        name="admin_panel_create_document_signing_requset",
    ),
    path(
        "edit_document/<str:id>",
        views.edit_document,
        name="admin_panel_edit_document",
    ),
    path("document/<str:id>", views.get_document, name="admin_panel_document"),
    path(
        "signed_documents/", views.signed_documents, name="admin_panel_signed_documents"
    ),
]
