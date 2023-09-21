from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from account_tiers.permissions import HasEnabledExpiringUrls

from .models import Image
from .serializers import ExpiringImageSerializer, ImageSerializer


class ImageListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ImageSerializer

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)


class ExpiringImageCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, HasEnabledExpiringUrls]
    serializer_class = ExpiringImageSerializer
