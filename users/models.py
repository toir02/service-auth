from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {
    'null': True,
    'blank': True
}


class User(AbstractUser):
    phone_number = models.CharField(
        max_length=12,
        verbose_name='Номер телефона',
        unique=True
    )
    invite_code = models.CharField(
        max_length=6,
        verbose_name='Инвайт-код',
        unique=True,
        **NULLABLE
    )
    activated_invite_code = models.CharField(
        max_length=6,
        verbose_name='Инвайт-код пригласившего',
        **NULLABLE
    )
    verification_code = models.CharField(
        max_length=4,
        verbose_name='Код верификации',
        **NULLABLE
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
