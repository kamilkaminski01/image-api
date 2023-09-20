from django.core.exceptions import ValidationError


def validate_thumbnail_sizes(data):
    if len(data) > 10:
        raise ValidationError("Thumbnail sizes must be a list of up to 10 integers.")
    elif len(data) != len(set(data)):
        raise ValidationError("Thumbnail sizes must contain unique integers.")
    for value in data:
        if not isinstance(value, int) or value < 200 or value > 1000:
            raise ValidationError(
                "Thumbnail sizes must be integers in the range of 200 to 1000."
            )
