import time

from rest_framework import (
    generics,
    status
)
from rest_framework.response import Response

from users.models import User
from users.permissions import IsUnauthenticated
from users.serializers import UserSerializer
from users.services import create_verification_code


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsUnauthenticated]

    def perform_create(self, serializer):
        verification_code = create_verification_code()
        password = self.request.data.get('password')

        user = serializer.save(verification_code=verification_code, is_active=False)
        user.set_password(str(password))
        user.save()

        # TODO send verification code to user phone number
        time.sleep(2)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
