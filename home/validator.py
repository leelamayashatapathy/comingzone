from rest_framework.validators import ValidationError


def no_digit(value):
    if any(char.isdigit() for char in value):
        raise ValidationError("Name shouldnot contain any digit")