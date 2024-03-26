from django import forms

from apps.base.widgets.select import Select


class ChoiceField(forms.ChoiceField):
    widget = Select
