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


def create_thumbnail_for_user(
    user: User, image: Image, filename: str, height: int
) -> Thumbnail:
    generated_thumbnail = generate_thumbnail(image.image.file, height, height)
    thumbnail = Thumbnail.objects.create(user=user, image=image)
    thumbnail.thumbnail.save(f"{height}px-{filename}", ContentFile(generated_thumbnail))
    return thumbnail
