from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm


def registration_view(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password1 = form.cleaned_data.get('password1')
        user.set_password(password1)
        user.save()
        new_user = authenticate(username=user.username, password1=password1)
        return redirect('accounts:login')

    return render(request, 'accounts/registration.html', {'form': form})
