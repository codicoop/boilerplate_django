import factory


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Faker("email", domain="example.com")
    password = factory.PostGenerationMethodCall("set_password", "password")

    class Meta:
        model = "users.User"
