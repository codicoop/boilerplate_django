from django.urls import reverse_lazy
from django.views.generic import RedirectView, TemplateView


class Home(RedirectView):
    url = reverse_lazy("login")
