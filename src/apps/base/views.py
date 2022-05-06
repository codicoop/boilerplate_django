from django.urls import NoReverseMatch, reverse, reverse_lazy
from django.utils.translation import get_language, activate
from django.views.generic import RedirectView, TemplateView
from django.utils.translation import gettext_lazy as _


class RootRedirectView(RedirectView):
    """
    If your site has an actual home page view that is not a redirect,
    you'll also need to move the URL in conf/urls.py from the urlpatterns
    block to the i18n_patterns one.
    """
    url = reverse_lazy("home")

    def get_redirect_url(self, *args, **kwargs):
        activate(get_language())
        return super().get_redirect_url(*args, **kwargs)


class HomeView(TemplateView):
    template_name = "home.html"


class StandardSuccess(TemplateView):
    template_name = "standard_success.html"
    link_text = _("Back")
    title = _("Registry successfully updated")
    success_title = _("Done!")
    description = _("The registry was updated correctly.")
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
