from django.urls import path

from .views import ExpiringImageCreateAPIView, ImageListCreateAPIView

urlpatterns = [
    path("", ImageListCreateAPIView.as_view(), name="images"),
    path("expire/", ExpiringImageCreateAPIView.as_view(), name="expiring_images"),
]
