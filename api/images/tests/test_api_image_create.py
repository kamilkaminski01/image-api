from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from account_tiers.tests.factories import AccountTierFactory
from images.models import Image
from images.tests.utils import generate_test_photo
from users.models import User


class TestImageCreateAPI(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.account_tier = AccountTierFactory()
        self.user = User.objects.create_user(
            email="test@user.com", password="password", account_tier=self.account_tier
        )
        self.url = reverse("images")
        self.client.login(email=self.user.email, password="password")

    def test_create_image(self):
        image = generate_test_photo()
        data = {"image": image}

        response = self.client.post(self.url, data, format="multipart")
        image_obj = Image.objects.first()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(image_obj.user, self.user)

    def test_create_image_unauthenticated(self):
        self.client.logout()

        image = generate_test_photo()
        data = {"image": image}

        response = self.client.post(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Image.objects.count(), 0)

    def test_create_image_invalid_image(self):
        invalid_image = SimpleUploadedFile(
            name="test.txt",
            content=b"This is not an image",
            content_type="text/plain",
        )

        data = {"image": invalid_image}

        response = self.client.post(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Image.objects.count(), 0)

    def test_create_image_large_file(self):
        self.client.login(email=self.user.email, password="password")

        large_image = SimpleUploadedFile(
            name="large_image.jpg",
            content=b"X" * (10 * 1024 * 1024),
            content_type="image/jpeg",
        )

        data = {"image": large_image}

        response = self.client.post(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Image.objects.count(), 0)
