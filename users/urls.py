from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from users.apps import UsersConfig
from users.views import (
    UserCreateAPIView,
    UserVerifyAPIView,
    UserRetrieveAPIView,
    ActivateInviteCodeAPIView
)

app_name = UsersConfig.name

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('create/', UserCreateAPIView.as_view(), name='create-user'),
    path('verify-user/<int:pk>/', UserVerifyAPIView.as_view(), name='verify-user'),
    path('view/<int:pk>/', UserRetrieveAPIView.as_view(), name='retrieve-user'),
    path('activate-invite-code/<int:pk>/', ActivateInviteCodeAPIView.as_view(), name='activate-invite-code'),
]
