from django import forms

from src.apps.demo.models import Data


class DataForm(forms.ModelForm):
    class Meta:
        model = Data
