# from itertools import chain

# from rest_framework import filters
from django_filters.rest_framework import FilterSet, filters

from user.models import CustomUser
from recipe.models import Recipe


# class IngredientFilter(filters.BaseFilterBackend):
#     """Фильтр ингредиентов по наименованию."""

#     def filter_queryset(self, request, queryset, view):
#         name_query_params = 'name'
#         value = request.query_params.get(name_query_params, None)
#         if value:
#             queryset_istartswith = queryset.filter(
#                 name__istartswith=value
#             )
#             queryset_contains = queryset.filter(
#                 name__contains=value
#             ).difference(queryset_istartswith).order_by(name_query_params)
#             return list(chain(queryset_istartswith, queryset_contains))
#         return queryset


class RecipeFilter(FilterSet):
    """Фильтр для рецептов."""

    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.ModelChoiceFilter(queryset=CustomUser.objects.all())
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
