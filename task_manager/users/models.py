from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


USERNAME_REGEX = r'^[a-zA-Zа-яА-Я0-9@.+-_]+\Z'


class User(AbstractUser):
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        blank=False,
        help_text='Обязательное поле. Не более 150 символов.',

    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        blank=False,
        help_text='Обязательное поле. Не более 150 символов.',

    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Имя пользователя',
        validators=[RegexValidator(USERNAME_REGEX)],
        help_text='Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.'
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['id']
