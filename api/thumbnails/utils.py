from io import BytesIO

from PIL import Image as PILImage


def generate_thumbnail(image_file: str, width: int, height: int):
    img = PILImage.open(image_file)
    img.thumbnail((width, height))
    thumbnail_io = BytesIO()
    img.save(thumbnail_io, format="JPEG")
    thumbnail_io.seek(0)
    return thumbnail_io.getvalue()
