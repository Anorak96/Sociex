from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password1',
            'password2',
        ]

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=30, help_text='Username cannot be edited.')

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'cover_pic',
            'profile_pic',
        ]