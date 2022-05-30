import logging

from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse_lazy


class UserValidatedMiddleware:
    """Checks whether the user, if not anonymous, is validated, and redirects
    accordingly."""

    logger = logging.getLogger("django.users")
    NON_VALIDATED_ALLOWED_PATHS = [
        reverse_lazy("registration:code_validation"),
        reverse_lazy("registration:logout"),
        reverse_lazy("registration:code_resend"),
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if self.non_validated_user(request):
            self.logger.info(
                "User hasn't been validated, redirecting to validation URL..."
            )
            return HttpResponseRedirect(reverse_lazy("registration:code_validation"))

        response = self.get_response(request)

        return response

    def non_validated_user(self, request: HttpRequest) -> bool:
        """Redirect if the user is not validated and trying to access a
        forbidden path."""
        return (
            request.user.is_authenticated
            and not request.user.is_validated
            and request.path not in self.NON_VALIDATED_ALLOWED_PATHS
        )
