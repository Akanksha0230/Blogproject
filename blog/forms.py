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

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

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
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'profile_image', 'phone_number','address']

    profile_image = forms.ImageField(required=True)
    phone_number = forms.CharField(required=True, max_length=10, min_length=10)
    address = forms.CharField(required=False, max_length=255)

class CustomPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        """
        Given an email, return matching user(s) who should receive a reset.
        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        User = get_user_model()
        active_users = User._default_manager.filter(**{
            '%s__iexact' % User.get_email_field_name(): email,
            'is_active': True,
        })
        return (u for u in active_users if u.has_usable_password())