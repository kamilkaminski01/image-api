from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from account_tiers.models import BasicAccountTierChoices
from account_tiers.tests.factories import AccountTierFactory
from images.models import Image
from images.tests.utils import generate_test_photo
from users.models import User


class TestExpiringImageCreateAPI(APITestCase):
    def setUp(self):
        self.client1 = APIClient()
        self.client2 = APIClient()
        self.account_tier_with_permissions = AccountTierFactory(
            enabled_expiring_urls=True
        )
        self.account_tier_without_permissions = AccountTierFactory(
            name=BasicAccountTierChoices.PREMIUM
        )
        self.user1 = User.objects.create_user(
            email="test1@user.com",
            password="password",
            account_tier=self.account_tier_with_permissions,
        )
        self.user2 = User.objects.create_user(
            email="test2@user.com",
            password="password",
            account_tier=self.account_tier_without_permissions,
        )
        self.url = reverse("expiring_images")
        self.image = generate_test_photo()
        self.client1.login(email=self.user1.email, password="password")
        self.client2.login(email=self.user2.email, password="password")

    def test_create_expiring_image(self):
        data = {"image": self.image, "url_expiration_time": 500}

        response = self.client1.post(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Image.objects.count(), 1)

        image_obj = Image.objects.first()
        self.assertEqual(image_obj.user, self.user1)
        self.assertIsNotNone(image_obj.url_expiration_time)

    def test_create_expiring_image_missing_expiration_time(self):
        data = {"image": self.image, "url_expiration_time": ""}
        response = self.client1.post(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_expiring_image_unauthenticated(self):
        self.client1.logout()
        data = {"image": self.image, "url_expiration_time": 500}
        response = self.client1.post(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_expiring_image_without_permissions(self):
        data = {"image": self.image, "url_expiration_time": 500}
        response = self.client2.post(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
