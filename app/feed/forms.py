from django import forms
from django.shortcuts import render


class PrescriptionForm(forms.Form):
    patient = forms.CharField(label='Patient Address', max_length=20)
    ndc = forms.CharField(label='National Drug Code', max_length=20)
    quantity = forms.CharField(label='Quantity', max_length=20)
    refills = forms.CharField(label='Refills', max_length=20)
