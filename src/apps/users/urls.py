from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from django.utils.translation import gettext_lazy as _

from apps.users.views import (
    details_view,
    EmailVerificationView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
    login_view,
    signup_view,
    SendVerificationCodeView,
)
from project.views import StandardSuccess

app_name = "registration"
urlpatterns = [
    # Registration
    path(_("sign-up/"), signup_view, name="signup"),
    path(_("sign-in/"), login_view, name="login"),
    path(
        _("log-out/"),
        auth_views.LogoutView.as_view(
            next_page=reverse_lazy("home"),
        ),
        name="logout",
    ),
    path(
        _("password-reset/"),
        PasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        _("password-reset/<uidb64>/<token>/"),
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        _("password-reset/done/"),
        PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        _("password-reset/complete/"),
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    # Profile
    path(
        _("profile/modified/"),
        StandardSuccess.as_view(
            url=reverse_lazy("registration:profile_details"),
        ),
        name="profile_details_success",
    ),
    path(
        _("profile/details/"),
        details_view,
        name="profile_details",
    ),
    path(
        _("user-validation/"),
        EmailVerificationView.as_view(),
        name="user_validation",
    ),
    path(
        _("send-verification-code/"),
        SendVerificationCodeView.as_view(),
        name="send_verification_code",
    ),
]
