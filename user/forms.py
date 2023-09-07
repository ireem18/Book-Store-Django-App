from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

import re


class PasswordChangeForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    new_password1 = forms.CharField(label='New Password')
    new_password2 = forms.CharField(label='Password Confirm')

    def clean(self):
        clean_data = super().clean()
        new_password1 = clean_data.get('new_password1')
        new_password2 = clean_data.get('new_password2')
        user = clean_data.get('username')
        try:
            User.objects.get(username=user)
        except Exception as e:
            raise forms.ValidationError("User not find!")

        if not re.match(new_password1, new_password2):
            raise forms.ValidationError("Passwords don't match")


User = get_user_model()
class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',)

    def clean(self):
        clean_data = super().clean()
        password1 = clean_data.get('password1')
        password2 = clean_data.get('password2')
        if not re.match(password1, password2):
            raise forms.ValidationError("Passwords don't match")
