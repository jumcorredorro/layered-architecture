from django.contrib.auth.models import User
from django import forms
from .models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email','username','password')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']

class UserLogin(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','password']
