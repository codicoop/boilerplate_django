from django import forms

from apps.demo.models import Data


class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        exclude = []
