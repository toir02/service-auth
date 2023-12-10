from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from users.models import User
from users.validators import PhoneNumberValidator


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'phone_number', 'is_active', 'verification_code')
        validators = [
            PhoneNumberValidator(field='phone_number')
        ]
