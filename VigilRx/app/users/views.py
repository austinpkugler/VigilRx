from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import CustomUserForm


def register(request):
    form = CustomUserForm()

    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account was successfully created.')
            return redirect('login')
    else:
        form = CustomUserForm()

    context = {'form': form}
    return render(request, 'users/register.html', context)


@login_required
def account(request):
    return render(request, 'users/account.html')
