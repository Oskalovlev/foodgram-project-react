from djoser.serializers import UserSerializer
from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователя и подписки."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name', 'is_subscribed',)

    def get_is_subscribed(self, author):
        """Проверка подписки пользователей."""

        request = self.context.get('request')
        return (request and request.user.is_authenticated
                and request.user.subscriber.filter(author=author).exists())
