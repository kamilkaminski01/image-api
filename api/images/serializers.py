from rest_framework import serializers

from .models import Image


class ImageListSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ["email", "image"]

    def get_email(self, obj: Image) -> str:
        return obj.user.email


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["image"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        image = Image.objects.create(**validated_data)
        return image