from itertools import islice

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    PasswordResetConfirmView as BasePasswordResetConfirmView,
    PasswordResetView as BasePasswordResetView,
)
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from apps.users.forms import (
    AuthenticationForm,
    PasswordResetForm,
    ProfileDetailsForm,
    UserSignUpForm,
)
from apps.users.models import User
from project.decorators import anonymous_required
from project.mixins import AnonymousRequiredMixin
from project.views import StandardSuccess


@anonymous_required
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("registration:profile_details")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


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
    if form.is_valid():
        form.save()
    return render(request, "profile/details.html", {"form": form})


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
