from typing import Dict

from rest_framework import serializers

from thumbnails.models import Thumbnail
from thumbnails.serializers import ThumbnailSerializer
from thumbnails.utils import create_thumbnail_for_user
from users.models import User

from .models import Image


class ImageListSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    thumbnails = ThumbnailSerializer(many=True, read_only=True)

    class Meta:
        model = Image
        fields = ["email", "image", "thumbnails"]

    def to_representation(self, instance):
        request = self.context.get("request")
        user = request.user

        if user.account_tier == User.AccountTierChoices.BASIC:
            thumbnail = instance.thumbnails.first()
            thumbnail_url = request.build_absolute_uri(thumbnail.thumbnail.url)
            return {
                "email": user.email,
                "thumbnails": {"thumbnail": thumbnail_url},
            }
        elif user.account_tier in [
            User.AccountTierChoices.PREMIUM,
            User.AccountTierChoices.ENTERPRISE,
        ]:
            thumbnails = Thumbnail.objects.filter(image=instance)
            thumbnails_data = [
                {"thumbnail": request.build_absolute_uri(thumbnail.thumbnail.url)}
                for thumbnail in thumbnails
            ]
            return {
                "email": user.email,
                "image": request.build_absolute_uri(instance.image.url),
                "thumbnails": thumbnails_data,
            }
        return super().to_representation(instance)


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
        basic_thumbnail = create_thumbnail_for_user(user, image, filename, 200)
        premium_thumbnail = create_thumbnail_for_user(user, image, filename, 400)
        if user.account_tier == User.AccountTierChoices.BASIC:
            return basic_thumbnail
        elif user.account_tier in [
            User.AccountTierChoices.PREMIUM,
            User.AccountTierChoices.ENTERPRISE,
        ]:
            return [image, basic_thumbnail, premium_thumbnail]

    def to_representation(self, instance):
        if isinstance(instance, Thumbnail):
            if request := self.context.get("request"):
                thumbnail_url = request.build_absolute_uri(instance.thumbnail.url)
                return {"thumbnail": thumbnail_url}
        elif isinstance(instance, list):
            if request := self.context.get("request"):
                image = instance.pop(0)
                thumbnails_data = [
                    {"thumbnail": request.build_absolute_uri(thumbnail.thumbnail.url)}
                    for thumbnail in instance
                ]
                return {
                    "image": request.build_absolute_uri(image.image.url),
                    "thumbnails": thumbnails_data,
                }
        return super().to_representation(instance)
