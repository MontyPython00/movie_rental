from django.shortcuts import render
from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout, authenticate

from accounts.forms import CreateAccountForm

# Create your views here.


class SignUpView(generic.CreateView):
    template_name = 'accounts/register.html'
    form_class = CreateAccountForm
    success_url = reverse_lazy('movie:home')


class SignInView(LoginView):
    template_name = 'accounts/login.html'
    next_page = reverse_lazy('movie:home')


class SignOutView(LogoutView):
    next_page = reverse_lazy('accounts:login')