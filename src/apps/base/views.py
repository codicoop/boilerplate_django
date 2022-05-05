from django.urls import NoReverseMatch, reverse, reverse_lazy
from django.views.generic import RedirectView, TemplateView


class Home(RedirectView):
    url = reverse_lazy("registration:login")


class StandardSuccess(TemplateView):
    template_name = "standard_success.html"
    link_text = "Tornar"
    title = "Dades actualitzades correctament"
    success_title = "Fet!"
    description = "Les dades han estat actualitzades correctament."
    url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        add_context = {
            "link_text": self.get_link_text(),
            "title": self.title,
            "success_title": self.success_title,
            "description": self.description,
            "url": self.get_url(),
        }
        context.update(add_context)
        return context

    def get_url(self):
        try:
            reversed_url = reverse(self.url)
        except NoReverseMatch:
            return self.url
        return reversed_url

    def get_link_text(self):
        return self.link_text
