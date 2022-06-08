"""
Local settings through django-environ
https://django-environ.readthedocs.io/en/latest/

Put the settings in /conf/.env
"""
import os

import environ
import sentry_sdk
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from sentry_sdk.integrations.django import DjangoIntegration

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()

##########################
#         Sentry         #
##########################
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

# False if not in os.environ
DEBUG = env("DEBUG")
# Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
# Instance's absolute URL (given we're not using Sites framework)
ABSOLUTE_URL = env("ABSOLUTE_URL")

# Variables for non-interactive superuser creation
DJANGO_SUPERUSER_EMAIL = env("DJANGO_SUPERUSER_EMAIL")
DJANGO_SUPERUSER_PASSWORD = env("DJANGO_SUPERUSER_PASSWORD")

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}
# If you enable this try a makemigrations to make sure the third party
# packages are not generating migrations.
# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Sendgrid
SENDGRID_API_KEY = env("SENDGRID_API_KEY", default="")
SENDGRID_SANDBOX_MODE_IN_DEBUG = env(
    "SENDGRID_SANDBOX_MODE_IN_DEBUG", bool, default=False
)
SENDGRID_TRACK_EMAIL_OPENS = env("SENDGRID_TRACK_EMAIL_OPENS", bool, default=False)
SENDGRID_TRACK_CLICKS_HTML = env("SENDGRID_TRACK_CLICKS_HTML", bool, default=False)
SENDGRID_TRACK_CLICKS_PLAIN = env("SENDGRID_TRACK_CLICKS_PLAIN", bool, default=False)

# SMTP
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env("EMAIL_USE_TLS", bool)
EMAIL_USE_SSL = env("EMAIL_USE_SSL", bool)
EMAIL_BACKEND = env("EMAIL_BACKEND")

# Celery
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default=None)

"""
Django settings for conf project.

Generated by 'django-admin startproject' using Django 2.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Application definition
INSTALLED_APPS = [
    "maintenance_mode",
    "constance.backends.database",
    "constance",
    "apps.base",
    "apps.users",
    "apps.celery",
    "django.contrib.postgres",
    "grappelli.dashboard",
    "grappelli",  # Place before contrib.admin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "post_office",
    "django_extensions",
]

AUTH_USER_MODEL = "users.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "login_required.middleware.LoginRequiredMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "maintenance_mode.middleware.MaintenanceModeMiddleware",
]

ROOT_URLCONF = "conf.urls"

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
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "conf.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE = "en"
LANGUAGES = [
    ("en", _("English")),
    ("ca", _("Catalan")),
]
TIME_ZONE = "Europe/Andorra"
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "src/static")
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "assets"),
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# For LoginRequiredMiddleware
# Using paths instead of view names so we can whitelist entire sections.
LOGIN_REQUIRED_IGNORE_PATHS = [
    r"^/admin/",
    r"/",
]

# Important settings, adjust according to your URLs:
LOGIN_URL = reverse_lazy("registration:login")
LOGIN_REDIRECT_URL = reverse_lazy("registration:profile_details")
LOGOUT_REDIRECT_URL = "/"

# Django Post Office
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
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default=None)


# Grappelli
GRAPPELLI_INDEX_DASHBOARD = "apps.base.dashboard.CustomIndexDashboard"

# Constance
CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
CONSTANCE_CONFIG = {"PROJECT_NAME": ("", _("Name of the website."))}
