# users/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)

class CustomSignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')