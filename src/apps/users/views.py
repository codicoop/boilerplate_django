from itertools import islice

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
)
from django.contrib.auth.views import (
    PasswordChangeView as BasePasswordChangeView,
)
from django.contrib.auth.views import (
    PasswordResetConfirmView as BasePasswordResetConfirmView,
)
from django.contrib.auth.views import (
    PasswordResetView as BasePasswordResetView,
)
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from apps.users.forms import (
    AuthenticationForm,
    EmailVerificationCodeForm,
    PasswordChangeForm,
    PasswordResetConfirmForm,
    PasswordResetForm,
    ProfileDetailsForm,
    SendVerificationCodeForm,
    UserSignUpForm,
)
from apps.users.services import send_confirmation_mail
from project.decorators import anonymous_required
from project.mixins import AnonymousRequiredMixin
from project.views import StandardSuccess


class LoginView(AnonymousRequiredMixin, BaseLoginView):
    template_name = "registration/login.html"
    success_url = reverse_lazy("registration:profile_details")
    form_class = AuthenticationForm


@anonymous_required
def signup_view(request):
    if request.method == "POST":
        form = UserSignUpForm(request.POST, None)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=email, password=password)
            login(request, user)
            return redirect("registration:profile_details")
    else:
        form = UserSignUpForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def details_view(request):
    form = ProfileDetailsForm(request.POST or None, instance=request.user)
    new_email = request.user.email
    if form.is_valid():
        user = form.save(commit=False)
        if new_email != user.email:
            user.email_verified = False
        user.save()
        return redirect("registration:profile_details_success")
    return render(request, "profile/details.html", {"form": form})


class EmailVerificationView(FormView, StandardSuccess):
    form_class = EmailVerificationCodeForm
    template_name = "registration/user_validation.html"
    success_url = reverse_lazy("registration:email_verification_complete")

    def form_valid(self, form):
        if (
            str(form.cleaned_data["email_verification_code"])
            == self.request.user.email_verification_code
        ):
            self.request.user.email_verified = True
            self.request.user.save()
            return super().form_valid(form)
        else:
            form.add_error(
                "email_verification_code",
                ValidationError(
                    "Code entered is not correct and the user cannot "
                    "be verified. Please try again."
                ),
            )
            return super().form_invalid(form)


class SendVerificationCodeView(FormView):
    template_name = "registration/send_verification_code.html"
    form_class = SendVerificationCodeForm
    success_url = reverse_lazy("registration:user_validation")

    def form_valid(self, form):
        send_confirmation_mail(self.request.user)
        return super().form_valid(form)


class EmailVerificationCompleteView(StandardSuccess):
    template_name = "standard_success.html"
    title = _("Done!")
    description = _("Account has been successfully verified.")
    url = reverse_lazy("registration:profile_details")
    link_text = _("Go back")


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
    form_class = PasswordResetConfirmForm
    template_name = "registration/password_reset_form.html"
    success_url = reverse_lazy("registration:password_reset_complete")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "validlink" not in context or not context["validlink"]:
            context["invalid_link"] = _("The link is invalid. Please try again.")
        return context


class PasswordResetDoneView(AnonymousRequiredMixin, StandardSuccess):
    template_name = "standard_success.html"
    title = _("Password reset sent")
    description = _(
        "An email has been sent to your inbox. "
        "Please check it and follow the instructions to "
        "change your password."
    )
    url = reverse_lazy("registration:login")
    link_text = _("Go back")


class PasswordResetCompleteView(AnonymousRequiredMixin, StandardSuccess):
    template_name = "standard_success.html"
    title = _("Password reset complete")
    description = _("Password reset complete")
    url = reverse_lazy("registration:login")
    link_text = _("Login")


class PasswordChangeView(BasePasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "registration/password_change_form.html"
    success_url = reverse_lazy("registration:password_change_done")


class PasswordChangeDoneView(StandardSuccess):
    template_name = "standard_success.html"
    title = _("Done!")
    description = _("Password change successful.")
    url = reverse_lazy("registration:profile_details")
    link_text = _("Go back")
