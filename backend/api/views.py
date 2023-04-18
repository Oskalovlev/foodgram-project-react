from django.db.models import Sum
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import response, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from .manage.functionality import add_and_del, out_list_ingredients
from .filters import IngredientFilter, RecipeFilter
from .pagination import LimitPageNumberPagination
from .permissions import IsAuthor
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeReadListSerializer,
                          ShoppingCartSerializer, SubscriptionSerializer,
                          TagSerializer, UserSerializer)
from recipe.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                           ShoppingCart, Tag)
from user.models import Subscription, User


class UserViewset(DjoserUserViewSet):
    """DjoserViewSet с управлением подпиской."""

    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    pagination_class = LimitPageNumberPagination

    @action(
        methods=('post', 'delete'),
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, **kwargs):
        """Управление подпиской."""

        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, id=author_id)
        if request.method == 'POST':
            serializer = SubscriptionSerializer(
                author,
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            Subscription.objects.create(user=user, author=author)
            return response.Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        get_object_or_404(
            Subscription,
            user=user,
            author=author
        ).delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=('get',),
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        """Возвращает авторов на которых подисан пользователь."""

        return self.get_paginated_response(
            SubscriptionSerializer(self.paginate_queryset(
                User.objects.filter(subscription_author__user=request.user)),
                many=True,
                context={'request': request},
            ).data
        )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet информации по тегам."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet информации по ингредиентам."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (IngredientFilter,)


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet информации по рецепту."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeReadListSerializer
    permission_classes = (IsAuthor,)
    pagination_class = LimitPageNumberPagination
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return RecipeCreateSerializer
        return RecipeReadListSerializer

    @action(
        methods=('post', 'delete',),
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        """Добавление/удаление рецепта в <избранное>."""

        return add_and_del(
            FavoriteSerializer, Favorite, request, pk
        )

    @action(
        methods=('post', 'delete',),
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        """Добавление/удаление рецепта в <список покупок>."""

        return add_and_del(
            ShoppingCartSerializer, ShoppingCart, request, pk
        )

    @action(
        methods=('get',),
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        """Выгрузка <спика покупок>."""

        ingredients = IngredientInRecipe.objects.filter(
            recipe__shopping_cart__user=self.request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).order_by('ingredient__name').annotate(amount=Sum('amount'))
        return out_list_ingredients(self, request, ingredients)
