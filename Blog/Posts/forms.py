# Django imports
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Third party imports
from ckeditor.widgets import CKEditorWidget

# Local imports
from .models import PostModel


class PostCreationForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ('title', 'body')

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'label': 'Title must be unique from other posts that had been posted to the website',
                }
            ),
            'body': CKEditorWidget(
                attrs={
                    'class': 'form-control',
                }
            )
        }