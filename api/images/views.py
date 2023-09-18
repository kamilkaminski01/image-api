from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer

from .models import Image
from .serializers import ImageListSerializer, ImageSerializer


class ImageListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)

    def get_serializer_class(self) -> ModelSerializer:
        if self.request.method == "POST":
            return ImageSerializer
        return ImageListSerializer
