from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, logout, login

from django.contrib.auth.models import User

from .forms import PasswordChangeForm, RegisterForm
from .decorators import authentication_not_required


@authentication_not_required
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('books')
        else:
            messages.warning(request, "Login Error! Username or password wrong!")
            return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@authentication_not_required
def forgot_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=form.cleaned_data.get('username'))
            if user:
                user.set_password(form.cleaned_data.get('new_password1'))
                user.save()
                messages.success(request, "Password updated!")
                return redirect('login')
            else:
                return HttpResponseRedirect('forgot_password')
        else:
            messages.info(request, "Please again..." + str(form.errors))
            return HttpResponseRedirect('forgot_password')
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'forgot_password.html', {'form': form})


@authentication_not_required
def create_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.set_password(form.cleaned_data.get('password1'))
            instance.save()
            return redirect('login')
        else:
            messages.info(request, "Please again..." + str(form.errors))
            return HttpResponseRedirect('create_user')
    else:
        form = PasswordChangeForm()
        return render(request, 'create_user.html', {'form': form})