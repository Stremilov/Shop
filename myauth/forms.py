from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

from myauth.models import Profile


class UserCreate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = 'username', 'first_name', 'email', 'bio', 'avatar'

    def send_info(self):
        data = self.cleaned_data
        return data