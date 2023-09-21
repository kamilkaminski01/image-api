import hashlib
from functools import partial
from pathlib import Path
from typing import IO

from django.core.exceptions import ValidationError
from django.db.models.fields.files import FieldFile


def hash_file(file: IO, block_size: int = 65536) -> str:
    hasher = hashlib.md5()
    for buf in iter(partial(file.read, block_size), b""):
        hasher.update(buf)
    return hasher.hexdigest()


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


def validate_url_expiration_time(value):
    if value < 300 or value > 30000:
        raise ValidationError("URL expiration time must be between 300 and 30000.")
