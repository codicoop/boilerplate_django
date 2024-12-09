from django import forms
from flowbite_classes.widgets import FlowBiteDateInput, FlowBiteTimeInput

from apps.demo.models import Data


class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = [
            "field_text_1",
            "field_text_2",
            "field_email",
            "field_radio",
            "field_boolean_checkbox",
            "field_select_dropdown",
            "field_password",
            "field_password_confirm",
            "field_number",
            "field_image",
            "field_file",
            "field_time",
            "field_date",
        ]
        widgets = {
            "field_password": forms.PasswordInput,
            "field_password_confirm": forms.PasswordInput,
            "field_radio": forms.RadioSelect,
            "field_time": FlowBiteTimeInput,
            "field_date": FlowBiteDateInput,
        }

    def clean(self):
        cleaned_data = super(DataForm, self).clean()
        password = cleaned_data.get("field_password")
        password_confirm = cleaned_data.get("field_password_confirm")
        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("The two password fields must match.")
        return cleaned_data
