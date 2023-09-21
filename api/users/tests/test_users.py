from django.contrib.auth import get_user_model
from django.test import TestCase

from account_tiers.models import BasicAccountTierChoices
from account_tiers.tests.factories import AccountTierFactory


class TestUserManager(TestCase):
    def setUp(self) -> None:
        self.account_tier = AccountTierFactory(name=BasicAccountTierChoices.ENTERPRISE)

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="normal@user.com", password="password", account_tier=self.account_tier
        )
        self.assertEqual(user.email, "normal@user.com")
        self.assertEqual(user.account_tier, self.account_tier)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_parms(self):
        User = get_user_model()
        with self.assertRaises(TypeError):
            User.objects.create_user()

    def test_create_user_without_email(self):
        User = get_user_model()
        with self.assertRaises(TypeError):
            User.objects.create_user(password="password")

    def test_create_user_without_password(self):
        User = get_user_model()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="normal@user.com")

    def test_create_user_with_empty_email(self):
        User = get_user_model()
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="password")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="super@user.com", password="password"
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
