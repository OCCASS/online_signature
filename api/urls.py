from django.urls import path
from . import views

urlpatterns = [path("send_sms/", views.SendSMSView.as_view(), name="api.send_messsage")]
