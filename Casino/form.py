from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Player


class PlayerRegistrationForm(UserCreationForm):
    class Meta:
        model = Player
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class PlayerBalanceForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['balance']
