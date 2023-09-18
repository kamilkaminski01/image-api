from django.urls import path

from .views import ImageListCreateAPIView

urlpatterns = [
    path("", ImageListCreateAPIView.as_view(), name="images"),
]
