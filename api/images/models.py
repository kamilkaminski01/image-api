from django.db import models

from users.models import User

from .utils import hash_file, validate_file_extension, validate_url_expiration_time


def _upload_image_to_images(instance, filename: str) -> str:
    hashed_file = hash_file(instance.image.open())
    return f"images/{instance.user.id}/{hashed_file}/{filename}"


class Image(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="images", verbose_name="user"
    )
    image = models.ImageField(
        upload_to=_upload_image_to_images,
        validators=[validate_file_extension],
        verbose_name="image",
    )

    url_expiration_time = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[validate_url_expiration_time],
        help_text="The time that an additional url of the image expires in seconds",
    )

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
