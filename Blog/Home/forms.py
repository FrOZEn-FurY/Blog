# Django imports
from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Search in titles',
            }
        ),
        required=False
    )

