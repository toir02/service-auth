from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from users.models import User
from users.validators import PhoneNumberValidator


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'phone_number', 'verification_code', 'is_active')
        validators = [
            PhoneNumberValidator(field='phone_number')
        ]


class ProfileSerializer(serializers.ModelSerializer):
    invited_users = SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'phone_number', 'invited_users', 'activated_invite_code', 'invite_code')

    def get_invited_users(self, obj):
        if obj.invite_code:
            invited_users = User.objects.filter(activated_invite_code=obj.invite_code)
            return [user.phone_number for user in invited_users]
        return []
