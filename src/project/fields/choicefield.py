from django import forms

from project.widgets.select import Select


class ChoiceField(forms.ChoiceField):
    widget = Select
