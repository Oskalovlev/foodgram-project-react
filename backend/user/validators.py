from django.core.exceptions import ValidationError


def username_validator(username):
    if username == 'me':
        raise ValidationError(
            ('Нельзя использовать это имя: "{username}"!')
        )
    return username
