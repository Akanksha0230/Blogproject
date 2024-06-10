from django import forms
from .models import Blog, Comment, User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from django.core.validators import RegexValidator, EmailValidator
from django.contrib.auth import get_user_model

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'image', 'content']

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.'
            )
        ]
    )
    email = forms.EmailField(
        required=True,
        validators=[EmailValidator(message='Enter a valid email address.')]
    )
    profile_image = forms.ImageField(required=True)
    phone_number = forms.CharField(required=True, max_length=10, min_length=10)
    address = forms.CharField(required=False, max_length=255)

    class Meta:
        model = User
        fields = ['username', 'email', 'profile_image', 'phone_number', 'address', 'password1', 'password2']
