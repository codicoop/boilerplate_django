import factory
from factory.django import DjangoModelFactory

from apps.users.models import UserManager, User


class UserManagerFactory(DjangoModelFactory):
    class Meta:
        model = UserManager


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email", domain="example.com")
