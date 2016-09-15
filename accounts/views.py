from django.shortcuts import render
from forms import RegistrationForm
from django.views.generic.edit import CreateView
from django.views.generic import FormView,RedirectView

from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm


from django.urls import reverse_lazy
# Create your views here.

class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = "account_views/register.html"
    success_url = reverse_lazy('login')


class LoginView(FormView):
    template_name = "account_views/login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("homepage")

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
    url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)