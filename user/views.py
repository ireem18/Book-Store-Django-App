from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, logout, login

from django.contrib.auth.models import User

from .forms import PasswordChangeForm, RegisterForm


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


def forgot_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        error = False
        if form.is_valid():
            new_password1 = form.cleaned_data.get('new_password1')
            new_password2 = form.cleaned_data.get('new_password2')
            user = User.objects.get(username=form.cleaned_data.get('username'))
            if not user:
                messages.info(request, "User not find!..." + str(form.errors))
                error = True
            if not new_password1 == new_password2:
                messages.info(request, "Passwords not same!..." + str(form.errors))
                error = True
            if not error:
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


def create_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        error = False
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('login')
        else:
            messages.info(request, "Please again..." + str(form.errors))
            return HttpResponseRedirect('create_user')
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'create_user.html', {'form': form})