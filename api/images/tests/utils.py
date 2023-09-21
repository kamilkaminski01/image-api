from io import BytesIO

from PIL import Image


def generate_test_photo():
    file = BytesIO()
    image = Image.new("RGB", size=(100, 100), color=(155, 0, 0))
    image.save(file, "png")
    file.name = "test.png"
    file.seek(0)
    return file
