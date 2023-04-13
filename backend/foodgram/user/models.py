from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name', )

    username = models.CharField(
        'Пользователь',
        max_length=settings.DATA_LENGTH_USER,
        unique=True,
        blank=False,
        validators=[RegexValidator(
            regex=r'^[\w$%^&#:;!]+\Z',
        )]
    )
    first_name = models.CharField(
        'Имя',
        max_length=settings.DATA_LENGTH_USER,
        blank=False,
        validators=[RegexValidator(
            regex=r'^[\w$%^&#:;!]+\Z',
        )]
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=settings.DATA_LENGTH_USER,
        blank=False,
        validators=[RegexValidator(
            regex=r'^[\w$%^&#:;!]+\Z',
        )]
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=settings.DATA_LENGTH_MAIL,
        unique=True,
        blank=False,
    )
    password = models.CharField(
        'Пароль',
        max_length=settings.DATA_LENGTH_USER,
        blank=False,
        null=False
    )

    class Meta(AbstractUser.Meta):
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """Модель подписки."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscription_author',
        verbose_name='Автор',
    )

    class Meta:
        ordering = ['user']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscribe'
            ),
            models.CheckConstraint(
                check=~models.Q(author=models.F('user')),
                name='check_author'),
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
