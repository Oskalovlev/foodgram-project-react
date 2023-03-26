from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CheckConstraint, F, Q, UniqueConstraint


class User(AbstractUser):
    """Модель пользователя."""
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Пользователь'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='Адрес электронной почты'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscriber(models.Model):
    """Модель подписки."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'following'],
                name='unique_follow'
            ),
            CheckConstraint(
                check=~Q(following=F('user')),
                name='check_following'),
        ]
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

    def __str__(self):
        return f'{self.user} подписан на {self.following}'
