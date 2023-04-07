from urllib.parse import unquote

from django.conf import settings
# from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from rest_framework import permissions, viewsets
from rest_framework.decorators import action

from .filters import RecipeFilter
from .pagination import LimitPageNumberPagination
from .permissions import IsAdmin, IsAuthor, IsReadOnly
from .serializers import (ShoppingCartSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeReadListSerializer,
                          TagSerializer, FavoriteSerializer)
from .manage.functionality import add_and_del, out_list_ingredients
from recipe.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                           ShoppingCart, Tag)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet информации по тегам."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet информации по ингредиентам."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    # filter_backends = (IngredientFilter,)
    pagination_class = None

    def get_queryset(self):
        """Получает ингредиент в соответствии с параметрами запроса."""

        name = self.request.query_params.get('name')
        # queryset = Ingredient.objects.all()
        queryset = self.queryset
        if name:
            if name[0] == '%':
                name = unquote(name)
            else:
                name = name.translate(settings.INCORRECT_LAYOUT)
            name = name.lower()
            start_queryset = list(queryset.filter(name__istartswith=name))
            ingridients_set = set(start_queryset)
            cont_queryset = queryset.filter(name__icontains=name)
            start_queryset.extend(
                [ing for ing in cont_queryset if ing not in ingridients_set]
            )
        return start_queryset


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet информации."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeReadListSerializer
    permission_classes = (IsAuthor,)
    pagination_class = LimitPageNumberPagination
    filterset_class = RecipeFilter
    # filter_backends = (DjangoFilterBackend, )

    # def perform_destroy(self, instance):
    #     instance.image.delete()
    #     instance.delete()

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return RecipeCreateSerializer
        return RecipeReadListSerializer

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def favorite(self, request, pk):
        return add_and_del(
            FavoriteSerializer, Favorite, request, pk
        )

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        """Добавляем/удаляем рецепт в 'список покупок'"""
        return add_and_del(
            ShoppingCartSerializer, ShoppingCart, request, pk
        )

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        ingredients = IngredientInRecipe.objects.filter(
            recipe__shopping_carts__user=self.request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).order_by('ingredient__name').annotate(amount=Sum('amount'))
        return out_list_ingredients(self, request, ingredients)
