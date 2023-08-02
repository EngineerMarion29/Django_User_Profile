from django import forms
from django.contrib.auth.models import User
from homepage.models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'