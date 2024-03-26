from django import forms


class CharField(forms.CharField):
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

    def get_bound_field(self, form, field_name):
        bound_field = super().get_bound_field(form, field_name)
        classes = self.widget.attrs.pop("class", "")
        if bound_field.errors:
            classes = " ".join((classes, self.error_classes))
        else:
            classes = " ".join((classes, self.no_error_classes))
        self.widget.attrs.update({"class": classes})
        return bound_field
