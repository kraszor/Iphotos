import re
from django.core.exceptions import ValidationError


def validate_hashtags(input):
    if not re.match('^(#\w+\S+)+$', input):
        raise ValidationError('Wrong format of tags!')