from djoser.views import UserViewSet as DjoserUserViewSet
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import response, status

from api.serializers import SubscriptionSerializer
from api.pagination import LimitPageNumberPagination
from user.models import CustomUser, Subscription
from user.serializers import CustomUserSerializer


class CustomUserViewset(DjoserUserViewSet):
    """
    DjoserViewSet стандартный.
    """
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = CustomUserSerializer
    pagination_class = LimitPageNumberPagination

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, **kwargs):
        """Подписываем / отписываемся на пользователя.
        Доступно только авторизованным пользователям.
        """
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(CustomUser, id=author_id)
        if request.method == 'POST':
            serializer = SubscriptionSerializer(
                author,
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            Subscription.objects.create(user=user, author=author)
            return response.Response(serializer.data,
                                     status=status.HTTP_201_CREATED)
        get_object_or_404(Subscription, user=user, author=author).delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        """Возвращает пользователей, на которых подписан текущий пользователь.
        В выдачу добавляются рецепты.
        """
        return self.get_paginated_response(
            SubscriptionSerializer(
                self.paginate_queryset(
                    CustomUser.objects.filter(author__user=request.user)
                ),
                many=True,
                context={'request': request},
            ).data
        )
