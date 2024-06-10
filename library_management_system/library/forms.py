# myapp/forms.py
from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Book


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'image_url', 'pdf_url', 'file']  # Include the file field
        

class PasswordResetForm(forms.Form):
    email = forms.EmailField()
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        data =  super().clean()
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        if new_password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return data