from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(UserCreationForm):
    class Meta:
        model= User
        fields=['username','email','password1','password2']

class CustomAuthenticateForm(AuthenticationForm):
    class Meta:
        model= User
        fields= ['username','password']

class SearchForm(forms.Form):
    searched = forms.CharField(max_length=100, required=False, label="Search")