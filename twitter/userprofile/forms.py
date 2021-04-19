from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import User, Tweet


class SignUpForm(UserCreationForm):
    email = forms.EmailField(help_text='Required. Please enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

class EditForm(ModelForm):
    image = forms.FileField(required=False)

    class Meta:
        model = User
        fields= ['biography', 'image']

class EditUserNameForm(ModelForm):
    class Meta:
        model = User
        fields= ['username']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class TweetForm(ModelForm):
    class Meta:
        model = Tweet
        fields = ('text', 'file')
