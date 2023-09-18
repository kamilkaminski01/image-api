from typing import Dict

from django.core.files.base import ContentFile
from rest_framework import serializers

from thumbnails.models import Thumbnail
from thumbnails.serializers import ThumbnailSerializer
from thumbnails.utils import generate_thumbnail
from users.models import User

from .models import Image


class ImageListSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    thumbnails = ThumbnailSerializer(many=True, read_only=True)

    class Meta:
        model = Image
        fields = ["email", "image", "thumbnails"]

    def get_email(self, obj: Image) -> str:
        return obj.user.email


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["image"]

    def create(self, validated_data: Dict) -> Image:
        user = self.context["request"].user
        validated_data["user"] = user
        image = Image.objects.create(**validated_data)
        if user.account_tier == User.AccountTierChoices.BASIC:
            height = 200
            thumbnail = generate_thumbnail(image.image, height, height)
            thumbnail_obj = Thumbnail.objects.create(user=user, image=image)
            thumbnail_obj.thumbnail.save(
                f"thumbnail-{height}x{height}.jpg", ContentFile(thumbnail)
            )
        return image
