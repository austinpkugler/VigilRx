from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect


class PrescriptionForm(forms.Form):
    npi = forms.CharField(label='National Provider Identifier', max_length=10)
    ndc = forms.CharField(label='National Drug Code', max_length=11)
    quantity = forms.CharField(label='Quantity', max_length=5)
    refills = forms.CharField(label='Refills', max_length=5)
