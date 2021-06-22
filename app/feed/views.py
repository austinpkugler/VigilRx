from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from . import bridge
from .forms import PrescriptionForm


def home(request):
    prescriptions = bridge.get_prescriptions()
    context = {
        'prescriptions': prescriptions
    }
    return render(request, 'feed/home.html', context)


def about(request):
    return render(request, 'feed/about.html', {'title': 'About'})


@login_required
def prescribe(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            bridge.create_prescription(form.cleaned_data)
        return redirect('feed-home')
    else:
        form = PrescriptionForm()
    return render(request, 'feed/prescribe.html', {'title': 'New Prescription', 'form': form})
