from django import forms

from apps.demo.models import Data


class DataForm(forms.ModelForm):
    field_radio = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=Data.RadioChoices.choices,
    )
    field_password = forms.CharField(
        widget=forms.PasswordInput(),
    )
    field_password_confirm = forms.CharField(
        widget=forms.PasswordInput(),
    )
    field_select_checkbox = forms.MultipleChoiceField(
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
