from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """
    Модель пользователя с правами администратора.
    """
    username = None
    email = models.EmailField(_("email address"), unique=True)

    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=100, verbose_name='страна', **NULLABLE)
    avatar = models.ImageField(upload_to='image_users/', verbose_name='аватар', **NULLABLE)

    token = models.CharField(max_length=100, verbose_name="Token", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
