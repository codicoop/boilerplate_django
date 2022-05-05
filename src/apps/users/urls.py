from django.urls import path
from django.utils.translation import gettext_lazy as _

from apps.users.views import PasswordResetView

app_name = "users"
urlpatterns = [
    path(
        _("password-reset/"),
        PasswordResetView.as_view(),
        name="password_reset",
    ),
]
