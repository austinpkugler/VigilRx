from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import CustomUserForm, CustomUserUpdateForm


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

    return render(request, 'users/register.html', {'form': form})


@login_required
def account(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('account')
    else:
        form = CustomUserUpdateForm(instance=request.user)

    return render(request, 'users/account.html', {'form': form})
