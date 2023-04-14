from urllib.parse import unquote
from itertools import chain
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import FilterSet, filters

from user.models import User
from recipe.models import Recipe


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


class IngredientFilter(SearchFilter):
    """Фильтр для ингредиентов."""

    def filter_queryset(self, request, queryset, view):

        name_query_params = 'name'
        value = request.query_params.get(name_query_params, None)
        if value:
            if value[0] == '%':
                value = unquote(value)
            else:
                value = value.translate(
                    str.maketrans(
                        'qwertyuiop[]asdfghjkl;\'zxcvbnm,./',
                        'йцукенгшщзхъфывапролджэячсмитьбю.'
                    )
                )
            value = value.lower()
            queryset_istartswith = queryset.filter(
                name__istartswith=value
            )
            queryset_contains = queryset.filter(
                name__contains=value
            ).difference(queryset_istartswith).order_by(name_query_params)
            return list(chain(queryset_istartswith, queryset_contains))
        return queryset
