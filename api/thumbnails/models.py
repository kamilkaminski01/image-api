from django.db import models

from images.models import Image
from images.utils import hash_file
from users.models import User


def _upload_thumbnail_to_images(instance, filename: str) -> str:
    hashed_file = hash_file(instance.image.image.open())
    return f"images/{instance.user.id}/{hashed_file}/{filename}"


class Thumbnail(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="thumbnails", verbose_name="user"
    )
    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name="thumbnails",
        verbose_name="image",
    )
    thumbnail = models.ImageField(upload_to=_upload_thumbnail_to_images)

    def __str__(self):
        return self.thumbnail.name

    class Meta:
        verbose_name = "Thumbnail"
        verbose_name_plural = "Thumbnails"
