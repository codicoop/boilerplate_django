from django.views.generic import FormView

from apps.demo.forms import DataForm


class DataView(FormView):
    template_name = "registration/home.html"
    form_class = DataForm
    success_url = ""
