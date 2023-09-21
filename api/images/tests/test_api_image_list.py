from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from account_tiers.tests.factories import AccountTierFactory
from images.models import Image
from users.models import User


class TestListImageAPI(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.account_tier = AccountTierFactory()
        self.user = User.objects.create_user(
            email="test@user.com", password="password", account_tier=self.account_tier
        )
        self.url = reverse("images")
        self.image1 = Image.objects.create(user=self.user, image="test_image1.jpg")
        self.image2 = Image.objects.create(user=self.user, image="test_image2.jpg")
        self.image3 = Image.objects.create(user=self.user, image="test_image3.jpg")
        self.client.login(email=self.user.email, password="password")

    def test_list_images(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_list_images_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
