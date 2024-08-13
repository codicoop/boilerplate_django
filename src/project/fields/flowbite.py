from django import forms
from django.db import models

from flowbite_classes.forms import (
    BooleanBoundField as FlowBiteBoundBooleanField,
    CharBoundField as FlowBiteBoundCharField
)

"""
The following is deprecated and not longer used. We should keep it only because
it's used in old migrations.

Migrations should be reset to be able to delete it.
"""


class FormCharField(forms.CharField):
    def get_bound_field(self, form, field_name):
        return FlowBiteBoundCharField(form, self, field_name)


class ModelCharField(models.CharField):
    def formfield(self, **kwargs):
        defaults = {"form_class": FormCharField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class FormPasswordField(forms.CharField):
    def get_bound_field(self, form, field_name):
        return FlowBiteBoundCharField(form, self, field_name)


class ModelPasswordField(models.CharField):
    def formfield(self, **kwargs):
        defaults = {"form_class": FormPasswordField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class FormIntegerField(forms.IntegerField):
    def get_bound_field(self, form, field_name):
        return FlowBiteBoundCharField(form, self, field_name)


class ModelIntegerField(models.IntegerField):
    def formfield(self, **kwargs):
        defaults = {"form_class": FormIntegerField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class FormRadioField(forms.ChoiceField):
    def get_bound_field(self, form, field_name):
        return FlowBiteBoundCharField(form, self, field_name)


class ModelRadioField(models.CharField):
    def formfield(self, **kwargs):
        defaults = {"form_class": FormRadioField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class FormSelectDropdownField(forms.ChoiceField):
    def get_bound_field(self, form, field_name):
        return FlowBiteBoundCharField(form, self, field_name)


class ModelSelectDropdownField(models.CharField):
    def formfield(self, **kwargs):
        defaults = {"form_class": FormSelectDropdownField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class FormSelectCheckboxField(forms.MultipleChoiceField):
    def get_bound_field(self, form, field_name):
        return FlowBiteBoundCharField(form, self, field_name)


class ModelSelectCheckboxField(models.CharField):
    def formfield(self, **kwargs):
        defaults = {"form_class": FormSelectCheckboxField}
        defaults.update(kwargs)
        return super(models.CharField, self).formfield(**defaults)


class FormEmailField(forms.EmailField):
    def get_bound_field(self, form, field_name):
        # Using FlowBiteBoundCharField instead of creating an
        # FlowBiteBoundEmailField as, for now, email fields use the same classes
        # as CharFields.
        return FlowBiteBoundCharField(form, self, field_name)


class ModelEmailField(models.EmailField):
    def formfield(self, **kwargs):
        defaults = {"form_class": FormEmailField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class FormBooleanField(forms.BooleanField):
    def get_bound_field(self, form, field_name):
        return FlowBiteBoundBooleanField(form, self, field_name)


class ModelBooleanField(models.BooleanField):
    def formfield(self, **kwargs):
        defaults = {"form_class": FormBooleanField}
        defaults.update(kwargs)
        return super().formfield(**defaults)
