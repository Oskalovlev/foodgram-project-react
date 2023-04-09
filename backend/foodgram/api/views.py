from urllib.parse import unquote

from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action

from .filters import RecipeFilter
from .pagination import LimitPageNumberPagination
from .permissions import IsAuthor
from .serializers import (ShoppingCartSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeReadListSerializer,
                          TagSerializer, FavoriteSerializer)
from .manage.functionality import add_and_del, out_list_ingredients
# from .manage import support_files
from recipe.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                           ShoppingCart, Tag)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet информации по тегам."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet информации по ингредиентам."""

    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    pagination_class = None

    def get_queryset(self):
        """Получение ингредиента."""

        name = self.request.query_params.get('name')
        queryset = Ingredient.objects.all()
        if name:
            if name[0] == '%':
                name = unquote(name)
            else:
                name = name.translate(
                    str.maketrans(
                        'qwertyuiop[]asdfghjkl;\'zxcvbnm,./',
                        'йцукенгшщзхъфывапролджэячсмитьбю.'
                    )
                )
            name = name.lower()
            start_queryset = list(queryset.filter(name__istartswith=name))
            ingridients_set = set(start_queryset)
            cont_queryset = queryset.filter(name__icontains=name)
            start_queryset.extend(
                [ing for ing in cont_queryset if ing not in ingridients_set]
            )
        return start_queryset


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
        detail=True,
        methods=('post', 'delete',),
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        return add_and_del(
            FavoriteSerializer, Favorite, request, pk
        )

    @action(
        detail=True,
        methods=('post', 'delete',),
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        """Добавление/удаление рецепта в <список покупок>."""
        return add_and_del(
            ShoppingCartSerializer, ShoppingCart, request, pk
        )

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        """Выгрузка <спика покупок>."""
        ingredients = IngredientInRecipe.objects.filter(
            recipe__shopping_carts__user=self.request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).order_by('ingredient__name').annotate(amount=Sum('amount'))
        return out_list_ingredients(self, request, ingredients)
