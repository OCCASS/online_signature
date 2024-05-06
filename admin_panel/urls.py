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
    path(
        "signed_documents/", views.signed_documents, name="admin_panel_signed_documents"
    ),
]
