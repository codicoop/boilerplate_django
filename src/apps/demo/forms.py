from django import forms
from django.utils.translation import gettext_lazy as _

from apps.demo.models import Data
from project.fields.flowbite import (
    FormBooleanField,
    FormCharField,
    FormEmailField,
    FormIntegerField,
    FormPasswordField,
    FormRadioField,
    FormSelectCheckboxField,
    FormSelectDropdownField,
)


class DataForm(forms.ModelForm):
    field_text_1 = FormCharField(
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "placeholder": _("Text 1"),
                "autocomplete": "text",
            }
        ),
        help_text="Help field_text_1",
    )
    field_text_2 = FormCharField(
        widget=forms.TextInput(
            attrs={"placeholder": _("Text 2"), "autocomplete": "text"}
        ),
        help_text="Help field_text_2",
    )
    field_email = FormEmailField(
        widget=forms.EmailInput(
            attrs={"autocomplete": "email", "placeholder": _("email address")}
        ),
        help_text="Help field_email",
    )
    field_radio = FormRadioField(
        widget=forms.RadioSelect,
        choices=Data.RadioChoices.choices,
        help_text="Help field_radio",
    )
    field_boolean_checkbox = FormBooleanField(
        widget=forms.CheckboxInput, help_text="Help field_boolean_checkbox"
    )

    field_password = FormPasswordField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password"},
            render_value=True,
        ),
        help_text="Help field_password",
    )
    field_password_confirm = FormPasswordField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password confirmation"},
            render_value=True,
        ),
        help_text="Help field_password_confirm",
    )
    field_number = FormIntegerField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": _("Number"),
                "autocomplete": "number",
            }
        ),
        help_text="Help field_number",
    )
    field_select_dropdown = FormSelectDropdownField(
        widget=forms.Select,
        choices=Data.SelectChoices.choices,
        help_text="Help field_select_dropdown",
    )
    field_select_checkbox = FormSelectCheckboxField(
        widget=forms.CheckboxSelectMultiple,
        choices=Data.SelectCheckboxChoices.choices,
        help_text="Help field_select_checkbox",
    )

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
            "field_select_checkbox",
        ]

    def clean(self):
        cleaned_data = super(DataForm, self).clean()
        password = cleaned_data.get("field_password")
        password_confirm = cleaned_data.get("field_password_confirm")
        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("The two password fields must match.")
        return cleaned_data
