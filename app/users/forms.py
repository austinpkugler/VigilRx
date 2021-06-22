from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role', 'address', 'identifier']

# class ProfileForm(ModelForm):
#     PATIENT, PRESCRIBER = 'patient', 'prescriber'
#     ROLE_CHOICES = (
#         (PATIENT, 'Patient'),
#         (PRESCRIBER, 'Prescriber'),
#     )
#     role = forms.ChoiceField(label='Role', choices=ROLE_CHOICES)
#     identifier = forms.CharField(label='National Provider Identifier', max_length=9)
#     address = forms.CharField(label='Address', max_length=42)

#     class Meta:
#         model = Profile
#         fields = ['role', 'identifier', 'address']

    # def save(self, commit=True):
    #     instance = super(ProfileForm, self).save(commit=False)
    #     instance.save()