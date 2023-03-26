from django.shortcuts import get_object_or_404
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class RecipeSerializer(serializers.ModelSerializer):
    """Серилайзер для модели Recipes."""
    # author = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='username'
    # )

    class Meta:
        model = Recipe
        fields = ['id', 'name']


class IngredientSerializer(serializers.ModelSerializer):
    """Серилайзер для модели Ingredient."""

    class Meta:
        model = Ingredient
        fields = ['id', 'name']


class TagSerializer(serializers.ModelSerializer):
    """Серилайзер для модели Tag."""

    class Meta:
        model = Tag
        fields = ['id', 'name']


class FavoriteSerializer(serializers.ModelSerializer):
    """Серилайзер для модели Favorite."""

    class Meta:
        model = Favorite
        fields = ('recipe', 'user')


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Серилайзер для модели ShoppingCart."""

    class Meta:
        model = ShoppingCart
        fields = ('')
