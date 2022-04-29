from django.urls import reverse_lazy
from django.views.generic import RedirectView


class Home(RedirectView):
    url = reverse_lazy("admin:login")
