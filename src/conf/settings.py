"""
Settings for the Django project.

For more information on Django's settings, visit:
    https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from pathlib import Path

import environ
import sentry_sdk
import structlog
from django.core.management.utils import get_random_secret_key
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from sentry_sdk.integrations.django import DjangoIntegration

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent

################################################################################
#                               General                                        #
################################################################################

# https://docs.djangoproject.com/en/4.2/ref/settings/#debug
DEBUG = env("DEBUG", default=False)

# https://docs.djangoproject.com/en/4.2/ref/settings/#secret-key
SECRET_KEY = env.str("SECRET_KEY", default=get_random_secret_key())

# https://docs.djangoproject.com/en/4.2/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

# https://docs.djangoproject.com/en/4.2/ref/settings/#csrf-trusted-origins
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

# Instance's absolute URL (given we're not using Sites framework)
ABSOLUTE_URL = env.str("ABSOLUTE_URL", default="")

# https://github.com/fabiocaccamo/django-maintenance-mode#settings
MAINTENANCE_MODE = env.bool("MAINTENANCE_MODE", default=False)
MAINTENANCE_MODE_STATE_BACKEND = "maintenance_mode.backends.DefaultStorageBackend"

# https://docs.djangoproject.com/en/4.2/ref/settings/#root-urlconf
ROOT_URLCONF = "conf.urls"

# https://docs.djangoproject.com/en/4.2/ref/settings/#wsgi-application
WSGI_APPLICATION = "conf.wsgi.application"


################################################################################
#                Internationalization and localization                         #
################################################################################

# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "Europe/Andorra"

# https://docs.djangoproject.com/en/4.2/ref/settings/#language-code
LANGUAGE_CODE = "ca"

# https://docs.djangoproject.com/en/4.2/ref/settings/#languages
LANGUAGES = [
    ("ca", _("Catalan")),
]

# https://docs.djangoproject.com/en/4.2/ref/settings/#use-i18n
USE_I18N = True

# https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-USE_TZ
USE_TZ = True

# https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-LOCALE_PATHS
LOCALE_PATHS = [str(BASE_DIR / "locale")]

# https://django-phonenumber-field.readthedocs.io/en/latest/reference.html#settings
# Setting these to 'national' is discouraged, but in our case it's unlikely this
# will arise in any problems.
PHONENUMBER_DEFAULT_REGION = "ES"
PHONENUMBER_DEFAULT_FORMAT = "NATIONAL"


################################################################################
#                               Databases                                      #
################################################################################

# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME", default=""),
        "USER": env("DB_USER", default=""),
        "PASSWORD": env("DB_PASSWORD", default=""),
        "HOST": env("DB_HOST", default=""),
        "PORT": env("DB_PORT", default=5432),
    }
}


################################################################################
#                                  Apps                                        #
################################################################################

# https://docs.djangoproject.com/en/4.2/ref/settings/#installed-apps
INSTALLED_APPS = [
    "maintenance_mode",
    "django.contrib.postgres",
    "grappelli.dashboard",
    "grappelli",  # Place before contrib.admin
    "constance.backends.database",
    "constance",
    "logentry_admin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "post_office",
    "django_extensions",
    "phonenumber_field",
    "apps.base",
    "apps.users",
    "apps.celery",
]


################################################################################
#                               Middleware                                     #
################################################################################

# https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-MIDDLEWARE
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "login_required.middleware.LoginRequiredMiddleware",
    "apps.users.middleware.UserValidatedMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "maintenance_mode.middleware.MaintenanceModeMiddleware",
]


################################################################################
#                             Authentication                                   #
################################################################################

# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"

# https://docs.djangoproject.com/en/4.2/ref/settings/#login-url
LOGIN_URL = reverse_lazy("auth:login")

# https://docs.djangoproject.com/en/4.2/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = reverse_lazy("home")

# https://docs.djangoproject.com/en/4.2/ref/settings/#logout-redirect-url
LOGOUT_REDIRECT_URL = "/"

# Setting for the LoginRequiredMiddleware middleware
# Using paths instead of view names so we can whitelist entire sections.
# https://github.com/CleitonDeLima/django-login-required-middleware#quick-start
LOGIN_REQUIRED_IGNORE_PATHS = [
    r"^/admin/",
    r"/",
]


################################################################################
#                               Passwords                                      #
################################################################################

# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"  # noqa
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


################################################################################
#                                Static                                        #
################################################################################

# https://docs.djangoproject.com/en/4.2/ref/settings/#static-root
STATIC_ROOT = str(BASE_DIR / "static")

# https://docs.djangoproject.com/en/4.2/ref/settings/#static-url
STATIC_URL = "/static/"

# https://docs.djangoproject.com/en/4.2/ref/settings/#staticfiles-dirs
STATICFILES_DIRS = [
    str(BASE_DIR / "assets"),
    str(BASE_DIR / "frontend" / "build" / "static"),
]

# https://docs.djangoproject.com/en/4.2/ref/settings/#staticfiles-storage
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


################################################################################
#                               Templates                                      #
################################################################################

# https://docs.djangoproject.com/en/4.2/ref/settings/#templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "maintenance_mode.context_processors.maintenance_mode",
                "constance.context_processors.config",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


################################################################################
#                               Media / Storage                                #
################################################################################

# https://docs.djangoproject.com/en/4.2/ref/settings/#media-root
MEDIA_ROOT = env.str("MEDIA_ROOT", default="")

# https://docs.djangoproject.com/en/4.2/ref/settings/#media-url
MEDIA_URL = env.str("MEDIA_URL", default="")

# Wasabi cloud storage configuration
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY", default="")
AWS_STORAGE_BUCKET_NAME = env.str("AWS_STORAGE_BUCKET_NAME", default="")
AWS_S3_ENDPOINT_URL = env.str("AWS_S3_ENDPOINT_URL", default="")
AWS_DEFAULT_ACL = env.str("AWS_DEFAULT_ACL", default="")
AWS_PUBLIC_MEDIA_LOCATION = env.str("AWS_PUBLIC_MEDIA_LOCATION", default="")
AWS_S3_BASE_DOMAIN = env.str("AWS_S3_BASE_DOMAIN", default="")
AWS_S3_CUSTOM_DOMAIN = f"{AWS_S3_BASE_DOMAIN}/{AWS_STORAGE_BUCKET_NAME}"
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
AWS_LOCATION = "static"
EXTERNAL_STATIC = AWS_S3_ENDPOINT_URL + "/" + AWS_STORAGE_BUCKET_NAME + "/local"
# In templates use {% external_static "/logo.png" %}
AWS_PRIVATE_MEDIA_LOCATION = env.str("AWS_PRIVATE_MEDIA_LOCATION", default="")


################################################################################
#                                  Email                                       #
################################################################################

# Post Office
# https://github.com/ui/django-post_office#settings
POST_OFFICE = {
    "BACKENDS": {
        "default": env(
            "POST_OFFICE_DEFAULT_BACKEND",
            default="django.core.mail.backends.console.EmailBackend",
        ),
    },
    "DEFAULT_PRIORITY": env("POST_OFFICE_DEFAULT_PRIORITY", default="now"),
    "MESSAGE_ID_ENABLED": True,
    "MESSAGE_ID_FQDN": env("POST_OFFICE_MESSAGE_ID_FQDN", default="example.com"),
    "CELERY_ENABLED": env("POST_OFFICE_CELERY_ENABLED", bool, default=False),
}

# https://docs.djangoproject.com/en/4.2/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default=None)

# Sendgrid
# https://github.com/sklarsa/django-sendgrid-v5#other-settings
SENDGRID_API_KEY = env("SENDGRID_API_KEY", default="")
SENDGRID_SANDBOX_MODE_IN_DEBUG = env(
    "SENDGRID_SANDBOX_MODE_IN_DEBUG", bool, default=False
)

# SMTP
# These are set to false as default given that Sendgrid's Web API is the default
# https://docs.djangoproject.com/en/4.2/ref/settings/#email
EMAIL_HOST = env.str("EMAIL_HOST", default="")
EMAIL_PORT = env.int("EMAIL_PORT", default="")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=False)
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=False)
EMAIL_BACKEND = env.str(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)


################################################################################
#                                  Admin                                       #
################################################################################

# Credentials for the initial superuser. Leave empty to skip its creation.
# Variables for non-interactive superuser creation
DJANGO_SUPERUSER_EMAIL = env("DJANGO_SUPERUSER_EMAIL", default=None)
DJANGO_SUPERUSER_PASSWORD = env("DJANGO_SUPERUSER_PASSWORD", default=None)


# Grappelli
# https://django-grappelli.readthedocs.io/en/latest/customization.html#available-settings
GRAPPELLI_INDEX_DASHBOARD = "apps.base.dashboard.CustomIndexDashboard"

# Constance
# https://django-constance.readthedocs.io/en/latest/#configuration
CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
DEFAULT_PROJECT_NAME = env.str("DEFAULT_PROJECT_NAME", default="")
CONSTANCE_CONFIG = {"PROJECT_NAME": (DEFAULT_PROJECT_NAME, _("Name of the website."))}


################################################################################
#                                  Logging                                     #
################################################################################

# https://docs.djangoproject.com/en/4.1/ref/logging/
DJANGO_LOG_LEVEL = env.str("DJANGO_LOG_LEVEL", default="WARNING").upper()
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "plain_console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(),
            "format": "{name} {levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "plain_console",
        },
    },
    "loggers": {
        # "django_structlog": {
        #     "handlers": ["console"],
        #     "level": "INFO",
        # },
        # Make sure to replace the following logger's name for yours
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
        structlog.dev.ConsoleRenderer(),
        # structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)


################################################################################
#                                  Celery                                      #
################################################################################

# We're using the only instance of Redis, but if we use caching in the future,
# we might want to set up two Redis servers and this will need to change.
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = env("REDIS_URL", default=None)


################################################################################
#                                Sentry                                        #
################################################################################

# https://docs.sentry.io/platforms/python/guides/django/
sentry_sdk.init(
    dsn=env("SENTRY_DSN", default=""),
    integrations=[DjangoIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)
