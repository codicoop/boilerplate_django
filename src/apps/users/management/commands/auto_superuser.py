import environ
from django.core.management.base import BaseCommand

from apps.users.models import User

env = environ.Env()
environ.Env.read_env()


class Command(BaseCommand):
    help = "Crea el superuser predeterminat sempre que no existeixi ja."

    def handle(self, *args, **options):
        DJANGO_SUPERUSER_EMAIL = env("DJANGO_SUPERUSER_EMAIL")
        DJANGO_SUPERUSER_PASSWORD = env("DJANGO_SUPERUSER_PASSWORD")

        if not User.objects.filter(email=DJANGO_SUPERUSER_EMAIL).exists():
            User.objects.create_superuser(
                email=DJANGO_SUPERUSER_EMAIL, password=DJANGO_SUPERUSER_PASSWORD
            )

        return 0
