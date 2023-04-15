from django.db.models import F
from django.db.transaction import atomic
from drf_extra_fields.fields import Base64ImageField
from rest_framework import (exceptions, fields, relations, serializers, status,
                            validators)

from recipe.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                           ShoppingCart, Tag)
from user.models import Subscription, User


class ShowRecipeAddedSerializer(serializers.ModelSerializer):
    """Сериализатор модели Recipe. Короткий, для некоторых эндпоинтов."""

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class TagSerializer(serializers.ModelSerializer):
    """Серилизатор модели Tag."""

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


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя и подписки."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name', 'is_subscribed',)

    def get_is_subscribed(self, author):
        """Проверка подписки пользователей."""

        request = self.context.get('request')
        return (request and request.user.is_authenticated
                and request.user.subscriber.filter(author=author).exists())


class RecipeReadListSerializer(serializers.ModelSerializer):
    """Серилизатор <списка> модели Recipes."""

    author = UserSerializer(read_only=True)
    image = Base64ImageField()
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = fields.SerializerMethodField(read_only=True)
    is_in_shopping_cart = fields.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'author',
            'image',
            'text',
            'tags',
            'cooking_time',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def get_ingredients(self, recipe):
        """Список ингредиентов."""

        return recipe.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('recipes__ingredient_list')
        )

    def get_is_favorited(self, obj):
        """Проверка избранного."""

        request = self.context.get('request')
        return (request and request.user.is_authenticated
                and request.user.favorites.filter(recipe=obj).exists())

    def get_is_in_shopping_cart(self, obj):
        """Проверка списка покупок."""

        request = self.context.get('request')
        return (request and request.user.is_authenticated
                and request.user.shopping_cart.filter(recipe=obj).exists())


class IngredientInRecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиента в рецепте."""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания рецептов."""

    author = UserSerializer(read_only=True)
    ingredients = IngredientInRecipeWriteSerializer(many=True)
    image = Base64ImageField(max_length=None, use_url=True)
    tags = relations.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )

    class Meta:
        model = Recipe
        fields = ('image', 'tags', 'author', 'ingredients',
                  'name', 'text', 'cooking_time')
        read_only_fields = ('author',)

    @atomic
    def create_bulk_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            IngredientInRecipe.objects.get_or_create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            )

    @atomic
    def create(self, validated_data):
        ingredients_list = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        author = self.context.get('request').user
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.save()
        recipe.tags.set(tags)
        self.create_bulk_ingredients(ingredients_list, recipe)
        return recipe

    @atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_bulk_ingredients(
            recipe=instance,
            ingredients=ingredients
        )
        return super().update(instance, validated_data)

    def validate_ingredients(self, value):
        """Проверяем ингредиенты в рецепте."""

        ingredients = self.initial_data.get('ingredients')
        if len(ingredients) <= 0:
            raise exceptions.ValidationError(
                {'ingredients': 'не может быть меньше 0'}
            )
        ingredients_list = []
        for item in ingredients:
            if item['id'] in ingredients_list:
                raise exceptions.ValidationError(
                    {'ingredients': 'не может повторятся'}
                )
            ingredients_list.append(item['id'])
            if int(item['amount']) <= 0:
                raise exceptions.ValidationError(
                    {'amount': 'не может быть меньше 0'}
                )
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

    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name',
                  'recipes', 'recipes_count',)
        read_only_fields = ('email', 'username', 'last_name', 'first_name',)

    def validate(self, data):
        """Наличие подписки пользователя c <исключением себя>."""

        author = self.instance
        user = self.context.get('request').user
        if Subscription.objects.filter(user=user, author=author).exists():
            raise exceptions.ValidationError(
                detail='Уже подписаны на пользователя',
                code=status.HTTP_400_BAD_REQUEST
            )
        if user == author:
            raise exceptions.ValidationError(
                detail='Нельзя подписаться на себя',
                code=status.HTTP_400_BAD_REQUEST
            )
        return data

    def get_recipes_count(self, obj):
        """Количество рецептов."""

        return obj.recipes.count()

    def get_recipes(self, obj):
        """Рецепты."""

        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit == int:
            try:
                recipes = recipes[:int(limit)]
            except ValueError:
                raise ('\nОжидеется тип даннх integer')
        serializer = ShowRecipeAddedSerializer(
            recipes,
            many=True,
            read_only=True
        )
        return serializer.data


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор модели Favorite."""

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'recipe'],
                message='Такой рецепт уже добавлен в избранное'
            )
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        return ShowRecipeAddedSerializer(
            instance.recipe,
            context={'request': request}
        ).data


class ShoppingCartSerializer(FavoriteSerializer):
    """Сериализатор модели ShoppingCart."""

    class Meta(FavoriteSerializer.Meta):
        model = ShoppingCart
        validators = [
            validators.UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=['user', 'recipe'],
                message='Такой рецепт уже добавлен в список'
            )
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        return ShowRecipeAddedSerializer(
            instance.recipe,
            context={'request': request}
        ).data
