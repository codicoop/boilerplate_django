from django import forms
from django.db import models
from icecream import ic

from project.fields.base import BaseFlowBiteBoundField


class FlowBiteBoundCharField(BaseFlowBiteBoundField):
    base_classes = "text-sm border rounded-lg block w-full p-2.5"
    no_error_classes = """
        bg-gray-50 border-gray-300 text-gray-900
        focus:ring-primary-600 focus:border-primary-600
        dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white
        dark:focus:ring-primary-500 dark:focus:border-primary-500
        """
    error_classes = """
        bg-red-50 border-red-500 text-red-900 placeholder-red-700
        focus:ring-red-500 focus:border-red-500
        dark:bg-gray-700 dark:text-red-500 dark:placeholder-red-500 dark:border-red-500
        """


class FlowBiteFormCharField(forms.CharField):
    def get_bound_field(self, form, field_name):
        return FlowBiteBoundCharField(form, self, field_name)


class FlowBiteModelCharField(models.CharField):
    def formfield(self, **kwargs):
        defaults = {"form_class": FlowBiteFormCharField}
        defaults.update(kwargs)
        return super().formfield(**defaults)
