from django.core.exceptions import ValidationError


def validate_no_hash(value):
    if "#" in value:
        raise ValidationError("error message")


def validate_no_numbers(value):
    for ch in value:
        if ch.isdigit():
            raise ValidationError("error message")


def validate_score(value):
    if 0 <= value <= 10:
        return
    else:
        raise ValidationError("error message")
