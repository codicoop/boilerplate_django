from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve, reverse


class VerificationRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        resolver = resolve(request.path)
        view_names = settings.VERIFICATION_REQUIRED_IGNORE_VIEW_NAMES
        if (
            request.user.is_authenticated
            and not request.user.email_verified
            and resolver.view_name not in view_names
        ):
            return redirect(reverse("registration:profile_details"))
        return self.get_response(request)
