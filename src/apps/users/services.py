from django.conf import settings
from .models import User
import random
from datetime import datetime, timedelta
from apps.base.post_office import send
from typing import Any
from django.conf import settings


def user_create(*, email: str, name: str, password: str, **kwargs: Any) -> User:
    """Handles the basic creation of a user by a non-staff agent."""
    user = User(email=email, name=name, password=password, **kwargs)
    user.set_password(password)
    user.full_clean()
    user.save()

    validation_email_send(user=user)

    return user


def validation_email_send(*, user: User) -> None:
    """Generates a code and sends a validation email."""
    # 1. Generate X-digit, calculate expiration date and save on the user
    code: int = generate_code()

    user.validation_code = code
    user.code_expires_at = datetime.now() + timedelta(days=1)
    user.save()

    # 2. Send to the user's email address
    context = {
        "project_name": "Codi Coop",
        "user_name": user.name,
        "date": datetime.today(),
        "time": datetime.now().time(),
        "user_email": user.email,
        "absolute_url": settings.ABSOLUTE_URL,
        "validation_code": user.validation_code,
        "expiration_date": user.code_expires_at,
    }
    send(
        recipients=[user.email],
        sender="no-reply@codi.coop",
        template="validation_code",
        priority="now",
        context=context,
    )


def generate_code() -> int:
    """Generates a pseudo-random 6-digit code."""
    return int("".join([str(random.randint(0, 9)) for i in range(6)]))
