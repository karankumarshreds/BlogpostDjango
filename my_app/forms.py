from django import forms
from .models import Profile
from django.contrib.auth.models import User


class UserUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username',]

class ProfileUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image',]