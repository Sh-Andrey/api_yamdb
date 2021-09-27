import datetime as dt

from django.core.exceptions import ValidationError


def validate_title_year(value):
    current_year = dt.datetime.now().year

    if value > current_year + 20:
        raise ValidationError(
            '%(value)s bad year',
            params={'value': value},
        )
