from urllib.parse import unquote

from django_filters.rest_framework import FilterSet, filters

from user.models import User
from recipe.models import Recipe, Ingredient


class RecipeFilter(FilterSet):
    """Фильтр для рецептов."""

    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(shopping_carts__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')


class IngredientFilter(FilterSet):
    """Фильтр для ингредиентов."""

    def filter_queryset(self, request):

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
            filtrated_queryset = list(queryset.filter(name__istartswith=name))
            ingridients_set = set(filtrated_queryset)
            cont_queryset = queryset.filter(name__icontains=name)
            filtrated_queryset.extend(
                [ing for ing in cont_queryset if ing not in ingridients_set]
            )
            return filtrated_queryset
        return queryset
