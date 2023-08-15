# Django imports
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class UserRegisterationForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    confpass = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'label': 'Confirm Password',
            }
        )
    )

    def clean(self):
        cd = super().clean()
        if cd['password'] and cd['confpass'] and cd['password'] != cd['confpass']:
            raise ValidationError(_('Passwords must match'))
        return cd


class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
