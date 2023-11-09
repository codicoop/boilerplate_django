from itertools import islice

# from django.contrib.auth.views import PasswordResetDoneView as BasePasswordResetDoneView # noqa
# from django.contrib.auth.views import (
#     PasswordResetCompleteView as BasePasswordResetCompleteView,
# )
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import (
    PasswordResetConfirmView as BasePasswordResetConfirmView,
)
from django.contrib.auth.views import PasswordResetView as BasePasswordResetView
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, UpdateView

from apps.base.mixins import AnonymousRequiredMixin
from apps.base.views import StandardSuccess
from apps.users.forms import (
    AuthenticationForm,
    PasswordResetForm,
    ProfileDetailsForm,
    UserSignUpForm,
)
from apps.users.models import User


class LoginView(AnonymousRequiredMixin, BaseLoginView):
    template_name = "registration/login.html"
    success_url = reverse_lazy("registation:profile_details")
    form_class = AuthenticationForm


class SignupView(FormView):
    template_name = "registration/signup.html"
    form_class = UserSignUpForm
    success_url = reverse_lazy("registration:code_validation")


class PasswordResetView(AnonymousRequiredMixin, BasePasswordResetView):
    form_class = PasswordResetForm
    template_name = "registration/password_reset_confirm.html"
    success_url = reverse_lazy("registration:password_reset_done")

    def form_valid(self, form):
        user = form.get_users(form.cleaned_data["email"])
        # get_users is a generator, but our email field is unique.
        # This is the simplest way to retrieve only 1 item from a generator:
        user_list = list(islice(user, 1))
        if len(user_list) == 0 or not user_list[0].is_active:
            error = ValidationError(
                _(
                    "El correu indicat no correspon a cap compte "
                    "registrat, si us plau verifica que l'hagis "
                    "escrit correctament."
                ),
                code="inexistent_email",
            )
            form.add_error(None, error)
            return super().form_invalid(form)
        return super().form_valid(form)


class PasswordResetConfirmView(AnonymousRequiredMixin, BasePasswordResetConfirmView):
    template_name = "registration/password_reset_form.html"
    success_url = reverse_lazy("registration:password_reset_complete")


class PasswordResetDoneView(AnonymousRequiredMixin, StandardSuccess):
    template_name = "standard_success.html"
    title = _("Password reset sent")
    description = _("Password reset sent")
    url = reverse_lazy("registration:login")
    link_text = _("Login")


class PasswordResetCompleteView(AnonymousRequiredMixin, StandardSuccess):
    template_name = "standard_success.html"
    title = _("Password reset complete")
    description = _("Password reset complete")
    url = reverse_lazy("registration:login")
    link_text = _("Login")


class DetailsView(UpdateView):
    template_name = "profile/details.html"
    form_class = ProfileDetailsForm
    model = User
    success_url = reverse_lazy("registration:profile_details_success")

    def get_object(self, queryset=None):
        return self.request.user
