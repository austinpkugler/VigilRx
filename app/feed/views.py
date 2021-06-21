from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import PrescriptionForm


prescriptions = [
    {
        'name': 'Aspirin',
        'ndc': '89342875',
        'prescriber': '0x89205A3A3b2A69De6Dbf7f01ED13B2108B2c43e7',
        'date': 'June 18, 2021'
    },
    {
        'name': 'Hydrocodone',
        'ndc': '532634634453',
        'prescriber': '0x89205A3A3b2A69De6Dbf7f01ED13B2108B2c43e7',
        'date': 'June 12, 2021'
    },
    {
        'name': 'Fentanyl',
        'ndc': '3253434553',
        'prescriber': '0x89205A3A3b2A69De6Dbf7f01ED13B2108B2c43e7',
        'date': 'November 18, 2020'
    }
]


def home(request):
    context = {
        'prescriptions': prescriptions
    }
    return render(request, 'feed/home.html', context)


def about(request):
    return render(request, 'feed/about.html', {'title': 'About'})


def prescribe(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
        return HttpResponseRedirect('')
    else:
        form = PrescriptionForm()
    return render(request, 'feed/prescribe.html', {'title': 'New Prescription', 'form': form})
