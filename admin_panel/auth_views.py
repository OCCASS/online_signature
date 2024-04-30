from . import forms

from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView as BaseLoginView
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy


class LoginView(BaseLoginView):
    redirect_authenticated_user = True
    template_name = "admin_panel/login.html"
    form_class = forms.LoginForm

    def get_success_url(self):
        return reverse_lazy("admin_panel_index")

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("admin_panel_login")
