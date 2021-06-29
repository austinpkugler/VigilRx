from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import CustomUser


class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'role', 'address', 'identifier', 'password1', 'password2']


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'role', 'address', 'contract', 'identifier']
