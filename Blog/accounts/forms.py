# Django imports
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


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

    def clean_confpass(self):
        password = self.cleaned_data['password']
        confpass = self.cleaned_data['confpass']
        if password and confpass and password != confpass:
            raise ValidationError(_('Passwords must match'))
        return confpass

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        if user:
            raise ValidationError(_('This username already exists'))
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user:
            raise ValidationError(_('This email already exists'))
        return email


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


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

        widgets = {
            'username': forms.TextInput(
              attrs={
                  'class': 'form-control',
              }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        similarity = User.objects.filter(email=email).exists()
        if similarity:
            raise ValidationError(_('The email you entered is already in use'))
        return email
