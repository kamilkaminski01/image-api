from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image as PILImage

from images.models import Image
from users.models import User

from .models import Thumbnail


def generate_thumbnail(image_file: str, width: int, height: int):
    img = PILImage.open(image_file)
    img.thumbnail((width, height))
    thumbnail_io = BytesIO()
    img.save(thumbnail_io, format="JPEG")
    thumbnail_io.seek(0)
    return thumbnail_io.getvalue()


def create_thumbnail_for_user(user: User, image: Image, filename: str):
    thumbnail_sizes = user.account_tier.thumbnail_sizes
    if isinstance(thumbnail_sizes, int):
        thumbnail_sizes = [thumbnail_sizes]
    for thumbnail_size in thumbnail_sizes:
        generated_thumbnail = generate_thumbnail(
            image.image.file, thumbnail_size, thumbnail_size
        )
        thumbnail = Thumbnail.objects.create(user=user, image=image)
        thumbnail.thumbnail.save(
            f"{thumbnail_size}px-{filename}", ContentFile(generated_thumbnail)
        )
    return image
