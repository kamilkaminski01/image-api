from django.db import models

from users.models import User

from .utils import validate_file_extension


def _upload_to_images(instance, filename: str) -> str:
    return f"images/{instance.user.id}/{filename}"


class Image(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_images", verbose_name="user"
    )
    image = models.ImageField(
        upload_to=_upload_to_images,
        validators=[validate_file_extension],
        verbose_name="image",
    )

    def __str__(self):
        return Image._meta.verbose_name.title()

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
