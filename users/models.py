from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=12, verbose_name='Номер телефона', unique=True)
    invite_code = models.CharField(max_length=6, verbose_name='Код приглашения', unique=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
