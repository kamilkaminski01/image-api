from typing import Dict

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from thumbnails.serializers import ThumbnailSerializer
from thumbnails.utils import create_thumbnail_for_user, rename_thumbnails_data

from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    thumbnails = ThumbnailSerializer(many=True, read_only=True)

    class Meta:
        model = Image
        fields = ["email", "image", "thumbnails"]

    def get_email(self, obj: Image) -> str:
        return obj.user.email

    def create(self, validated_data: Dict) -> Image:
        user = self.context["request"].user
        validated_data["user"] = user
        filename = validated_data["image"].name
        image = Image.objects.create(**validated_data)
        return create_thumbnail_for_user(user, image, filename)

    def to_representation(self, instance) -> Dict:
        user = self.context["request"].user
        data = super().to_representation(instance)
        thumbnails_data = data.get("thumbnails", [])
        data["thumbnails"] = rename_thumbnails_data(thumbnails_data)
        if not user.account_tier.include_original_image_url:
            del data["image"]
        return data


class ExpiringImageSerializer(serializers.ModelSerializer):
    expiring_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ["image", "url_expiration_time", "expiring_url"]

    def create(self, validated_data: Dict):
        user = self.context["request"].user
        filename = validated_data["image"].name
        validated_data["user"] = user
        image = Image.objects.create(**validated_data)
        create_thumbnail_for_user(user, image, filename)
        return image

    def validate_url_expiration_time(self, value):
        if value is None:
            raise ValidationError("URL expiration time is required")
        else:
            return value

    def get_expiring_url(self, obj):
        expiration_time = obj.url_expiration_time
        return f"{obj}/?expires={expiration_time}"
