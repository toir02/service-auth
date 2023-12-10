import time

from rest_framework import (
    generics,
    status
)
from rest_framework.response import Response

from users.models import User
from users.permissions import IsUnauthenticated
from users.serializers import RegisterSerializer
from users.services import (
    create_verification_code,
    create_invite_code
)


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
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


class UserVerifyView(generics.UpdateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsUnauthenticated]
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        invite_code = create_invite_code()

        while User.objects.filter(invite_code=invite_code).exists():
            invite_code = create_invite_code()

        instance.invite_code = invite_code
        instance.is_active = True
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
