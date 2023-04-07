
from django.conf import settings
from django.db import models, transaction
from rest_framework import (exceptions, fields, relations, serializers, status,
                            validators)
# from rest_framework.exceptions import ValidationError

from recipe.models import (Ingredient, IngredientInRecipe, Recipe,
                           Tag, Favorite, ShoppingCart)
from user.models import Subscription, CustomUser
from user.serializers import CustomUserSerializer
from .manage.support_files import Base64ImageField


class ShowRecipeAddedSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe.
    Определён укороченный набор полей для некоторых эндпоинтов."""

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class TagSerializer(serializers.ModelSerializer):
    """Серилизатор модели Tag."""

    slug = serializers.SlugField(
        max_length=200,
        validators=[
            validators.UniqueValidator(queryset=Tag.objects.all())
        ]
    )

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Серилизатор модели Ingredient."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """ Сериализатор модели IngredientInRecipe."""

    id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='ingredient'
    )
    name = serializers.SlugRelatedField(
        source='ingredient',
        read_only=True,
        slug_field='name'
    )
    measurement_unit = serializers.SlugRelatedField(
        source='ingredient',
        read_only=True,
        slug_field='measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = '__all__'


class RecipeReadListSerializer(serializers.ModelSerializer):
    """Серилизатор списка модели Recipes."""

    author = CustomUserSerializer()
    image = Base64ImageField()
    ingredients = IngredientInRecipeSerializer(many=True,
                                               required=True,
                                               source='ingredient_list')
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = fields.SerializerMethodField(read_only=True)
    is_in_shopping_cart = fields.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',
        )

    def get_ingredients(self, recipe):
        """Получает список ингредиентов для рецепта."""
        return recipe.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=models.F('recipes__ingredient_list')
        )

    def get_is_favorited(self, obj):
        """Проверка - находится ли рецепт в избранном."""
        request = self.context.get('request')
        return (request and request.user.is_authenticated
                and request.user.favorites.filter(recipe=obj).exists())

    def get_is_in_shopping_cart(self, obj):
        """Проверка - находится ли рецепт в списке покупок."""
        request = self.context.get('request')
        return (request and request.user.is_authenticated
                and request.user.shopping_carts.filter(recipe=obj).exists())


class IngredientInRecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиента в рецепте."""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создание рецептов."""

    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientInRecipeWriteSerializer(many=True)
    image = Base64ImageField(max_length=None, use_url=True)
    tags = relations.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )

    class Meta:
        model = Recipe
        fields = ('id', 'image', 'tags', 'author', 'ingredients',
                  'name', 'text', 'cooking_time')
        read_only_fields = ('author',)

    @transaction.atomic
    def create_bulk_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            IngredientInRecipe.objects.get_or_create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            )

    @transaction.atomic
    def create(self, validated_data):
        ingredients_list = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        author = self.context.get('request').user
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.save()
        recipe.tags.set(tags)
        self.create_bulk_ingredients(ingredients_list, recipe)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_bulk_ingredients(recipe=instance,
                                     ingredients=ingredients)
        return super().update(instance, validated_data)

    def validate_ingredients(self, value):
        """Проверяем ингредиенты в рецепте."""
        ingredients = self.initial_data.get('ingredients')
        if len(ingredients) <= 0:
            raise exceptions.ValidationError(
                {'ingredients': settings.INGREDIENT_MIN_AMOUNT_ERROR}
            )
        ingredients_list = []
        for item in ingredients:
            if item['id'] in ingredients_list:
                raise exceptions.ValidationError(
                    {'ingredients': settings.INGREDIENT_DUBLICATE_ERROR}
                )
            ingredients_list.append(item['id'])
            if int(item['amount']) <= 0:
                raise exceptions.ValidationError(
                    {'amount': settings.INGREDIENT_MIN_AMOUNT_ERROR}
                )
        return value

    def validate_cooking_time(self, data):
        """Проверяем время приготовления рецепта."""
        cooking_time = self.initial_data.get('cooking_time')
        if int(cooking_time) <= 0:
            raise serializers.ValidationError(
                settings.COOKING_TIME_MIN_ERROR
            )
        return data

    def validate_tags(self, value):
        """Проверяем на наличие уникального тега."""
        tags = value
        if not tags:
            raise exceptions.ValidationError(
                {'tags': settings.TAG_ERROR}
            )
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise exceptions.ValidationError(
                    {'tags': settings.TAG_UNIQUE_ERROR}
                )
            tags_list.append(tag)
        return value

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeReadListSerializer(
            instance, context=context
        ).data


class SubscriptionSerializer(serializers.ModelSerializer):
    """Серилизатор подписки."""

    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta(CustomUserSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name', 'is_subscribed',
                  'recipes', 'recipes_count',)
        read_only_fields = ('email', 'username', 'last_name', 'first_name',)

    def validate(self, data):
        """Проверяем наличие подписки у пользователя и отсекаем самого себя."""
        author = self.instance
        user = self.context.get('request').user
        if Subscription.objects.filter(user=user, author=author).exists():
            raise exceptions.ValidationError(
                detail=settings.DUBLICAT_USER,
                code=status.HTTP_400_BAD_REQUEST
            )
        if user == author:
            raise exceptions.ValidationError(
                detail=settings.SELF_FOLLOW,
                code=status.HTTP_400_BAD_REQUEST
            )
        return data

    def get_recipes_count(self, obj):
        """Достаем количество рецептов."""
        return obj.recipes.count()

    def get_recipes(self, obj):
        """Достаем рецепты."""
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = ShowRecipeAddedSerializer(recipes,
                                               many=True,
                                               read_only=True)
        return serializer.data


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор добавления/удаления рецепта в избранное."""

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'recipe'],
                message=settings.RECIPE_IN_FAVORITE
            )
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        return ShowRecipeAddedSerializer(
            instance.recipe,
            context={'request': request}
        ).data


class ShoppingCartSerializer(FavoriteSerializer):
    """Сериализатор добавления рецептов в список покупок."""

    class Meta(FavoriteSerializer.Meta):
        model = ShoppingCart
        validators = [
            validators.UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=['user', 'recipe'],
                message=settings.ALREADY_BUY
            )
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        return ShowRecipeAddedSerializer(
            instance.recipe,
            context={'request': request}
        ).data
