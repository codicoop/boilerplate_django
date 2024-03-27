from django import forms


class BaseFlowBiteBoundField(forms.BoundField):
    base_classes = ""
    no_error_classes = ""
    error_classes = ""

    def css_classes(self, extra_classes=None):
        classes = super().css_classes(extra_classes).split()
        classes.append(self.base_classes)
        if self.errors:
            classes.append(self.error_classes)
        else:
            classes.append(self.no_error_classes)
        return " ".join(classes)

    def get_context(self):
        ctxt = super().get_context()
        widget = ctxt["field"].field.widget
        widget.attrs["class"] = self.css_classes()
        return ctxt


class FlowBiteCharField(BaseFlowBiteBoundField):
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


class CharField(forms.CharField):
    def get_bound_field(self, form, field_name):
        return FlowBiteCharField(form, self, field_name)
