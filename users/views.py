import time

from rest_framework import (
    generics,
    status
)
from rest_framework.response import Response

from users.models import User
from users.permissions import IsUnauthenticated
from users.serializers import RegisterSerializer, ProfileSerializer
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


class UserVerifyAPIView(generics.UpdateAPIView):
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


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()


class ActivateInviteCodeAPIView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        invite_code_to_activate = self.request.data.get("invite_code")

        if not invite_code_to_activate:
            return Response({'error': 'Invite code to activate is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = User.objects.get(invite_code=invite_code_to_activate)
        except User.DoesNotExist:
            return Response({'error': 'Invalid invite code.'}, status=status.HTTP_400_BAD_REQUEST)

        if user.activated_invite_code:
            return Response({'error': 'User has already activated an invite code.'}, status=status.HTTP_400_BAD_REQUEST)

        user.activated_invite_code = invite_code_to_activate
        user.save()

        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
