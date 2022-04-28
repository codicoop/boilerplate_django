from django.test import TestCase
from apps.users.models import User

class UsersTestCase(TestCase):
    def setUp(self):
        pass

    def test_email_required(self):
        """"Email is required for user creation."""
        with self.assertRaisesMessage(TypeError, "email"):
            User.objects.create_user()

        with self.assertRaisesMessage(ValueError, "Users must have an email address"):
            User.objects.create_user(email=None)

class SuperusersTestCase(TestCase):
    def setUp(self):
        self.email = "admin@admin.com"
        self.password = "admin"

    def test_password_required(self):
        """Password is required for superuser creation."""
        with self.assertRaisesMessage(TypeError, "password"):
            User.objects.create_superuser(email=self.email)

        with self.assertRaisesMessage(ValueError, "Superusers must have a password"):
            User.objects.create_superuser(email=self.email, password=None)
            
        with self.assertRaisesMessage(ValueError, "Superusers must have a password"):
            User.objects.create_superuser(email=self.email, password="")

    def test_is_staff(self):
        """Method create_superuser must make is_staff True."""
        user: User = User.objects.create_superuser(email=self.email, password=self.password)
        self.assertTrue(user.is_staff)

    def test_is_superuser(self):
        """Method create_superuser must make is_superuser True."""
        user: User = User.objects.create_superuser(email=self.email, password=self.password)
        self.assertTrue(user.is_superuser)