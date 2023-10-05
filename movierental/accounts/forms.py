from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CreateAccountForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginView(forms.Form):
    login = forms.CharField(label='Login', min_length=4, max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Insert login'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Insert password'}))