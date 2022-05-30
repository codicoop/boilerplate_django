from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
import logging


class UserValidatedMiddleware:
    """Checks whether the user, if not anonymous, is validated, and redirects
    accordingly."""

    logger = logging.getLogger("django.users")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Redirect if the user is authenticated but not validated
        # only if it's not being redirected already.
        if (
            request.user.is_authenticated
            and not request.user.is_validated
            and request.path != reverse_lazy("registration:code_validation")
            and request.path != reverse_lazy("registration:logout")
            and request.path != reverse_lazy("registration:code_resend")
        ):
            self.logger.info(
                "User hasn't been validated, redirecting to validation URL..."
            )
            return HttpResponseRedirect(reverse_lazy("registration:code_validation"))

        response = self.get_response(request)

        return response
