from pathlib import Path

from django.core.exceptions import ValidationError
from django.db.models.fields.files import FieldFile


def get_file_extension(filename: str) -> str:
    return Path(filename).suffix.lower()


def validate_file_extension(value):
    extension = get_file_extension(value.name)
    valid_extensions = [".png", ".jpg", ".jpeg"]
    if extension not in valid_extensions:
        raise ValidationError("File not supported")


def does_file_exist(file: FieldFile) -> bool:
    if file.url.startswith("/media"):
        try:
            open(file.url)
        except FileNotFoundError:
            return False
    return True
