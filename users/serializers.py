from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from users.models import User
from users.validators import PhoneNumberValidator


class UserSerializer(serializers.ModelSerializer):
    invited_users = SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'
        validators = [
            PhoneNumberValidator(field='phone_number')
        ]

    def get_invited_users(self, obj):
        if obj.invite_code:
            invited_users = User.objects.filter(invite_code=obj.invite_code)
            return UserSerializer(invited_users, many=True).data
        return []
