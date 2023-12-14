import re

from rest_framework.exceptions import ValidationError


class PhoneNumberValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        phone_number = value.get(self.field)
        if not re.match(r'^(?:\+7\d{10}|89\d{9})$', phone_number):
            raise ValidationError("Invalid phone number format")
