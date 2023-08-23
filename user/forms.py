from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PasswordChangeForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    new_password1 = forms.CharField(label='New Password')
    new_password2 = forms.CharField(label='Password Confirm')


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',)

