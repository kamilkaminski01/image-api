from typing import Dict

from rest_framework import serializers

from thumbnails.serializers import ThumbnailSerializer
from thumbnails.utils import create_thumbnail_for_user

from .models import Image


class ImageListSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    thumbnails = ThumbnailSerializer(many=True, read_only=True)

    class Meta:
        model = Image
        fields = ["email", "image", "thumbnails"]

    def get_email(self, obj: Image) -> str:
        return obj.user.email

    def to_representation(self, instance):
        user = self.context["request"].user
        data = super().to_representation(instance)
        if not user.account_tier.include_original_image_url:
            del data["image"]
        return data


class ImageSerializer(serializers.ModelSerializer):
    thumbnails = ThumbnailSerializer(many=True, read_only=True)

    class Meta:
        model = Image
        fields = ["image", "thumbnails"]

    def create(self, validated_data: Dict):
        user = self.context["request"].user
        validated_data["user"] = user
        filename = validated_data["image"].name
        image = Image.objects.create(**validated_data)
        return create_thumbnail_for_user(user, image, filename)

    def to_representation(self, instance):
        user = self.context["request"].user
        data = super().to_representation(instance)
        if not user.account_tier.include_original_image_url:
            del data["image"]
        return data
