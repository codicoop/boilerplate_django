from .settings import *  # noqa

DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:", "TEST": {}}
}
WHITENOISE_AUTOREFRESH = env.bool("WHITENOISE_AUTOREFRESH", default=DEBUG)
