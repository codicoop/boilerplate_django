from django.test import TestCase

from tests.factories.users import UserFactory


class EnquiryAnswerCreateViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def test_demo(self):
        print(self.user)
