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
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'style': 'padding: 5px; resize: none; border-color: black;'}), required=False)
    email = forms.CharField(required=False)


    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'bio',
            'cover_pic',
            'profile_pic',
        ]