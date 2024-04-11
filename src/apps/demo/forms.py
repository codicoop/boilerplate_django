from django import forms

from apps.demo.models import Data
from project.fields.flowbite import (
    FormPasswordField,
    FormRadioField,
    FormSelectDropdownField,
    FormSelectCheckboxField,
)


class DataForm(forms.ModelForm):
    field_radio = FormRadioField(
        widget=forms.RadioSelect,
        choices=Data.RadioChoices.choices,
    )
    field_password = FormPasswordField(
        widget=forms.PasswordInput(),
    )
    field_password_confirm = FormPasswordField(
        widget=forms.PasswordInput(),
    )
    field_select_dropdown = FormSelectDropdownField(
        widget=forms.Select,
        choices=Data.SelectChoices.choices,
    )
    field_select_checkbox = FormSelectCheckboxField(
        widget=forms.CheckboxSelectMultiple,
        choices=Data.SelectCheckboxChoices.choices
    )

    class Meta:
        model = Data
        exclude = []

    def clean(self):
        cleaned_data = super(DataForm, self).clean()
        password = cleaned_data.get('field_password')
        password_confirm = cleaned_data.get('field_password_confirm')
        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("The two password fields must match.")
        return cleaned_data
