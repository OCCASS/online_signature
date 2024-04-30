from django.urls import path
from . import views


urlpatterns = [
    path("", views.index_view, name="index"),
    path("document/<str:id>", views.document_view, name="document"),
]
