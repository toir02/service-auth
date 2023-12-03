from rest_framework import serializers

from users.models import User
from users.validators import PhoneNumberValidator


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        validators = [
            PhoneNumberValidator(field='phone_number')
        ]
