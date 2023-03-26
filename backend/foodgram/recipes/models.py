from django.db import models
from users.models import User


class Tag(models.Model):
    """Модель тэгов."""
    name = models.CharField(max_length=200)
    color = models.CharField(
        max_length=7,
        default="#ffffff"
    )
    slug = models.SlugField(max_length=200)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название продукта'
    )
    measurement_unit = models.SlugField(
        max_length=200,
        verbose_name='Единица измерения'
    )
    amount = models.PositiveIntegerField(
        blank=True,
        null=True,
        default=0
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
        )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='recipes',
        verbose_name='Ингредиент'
    )
    text = models.TextField(verbose_name='Описание')
    image = models.ImageField(
        upload_to='recipes/',
        null=True,
        blank=True,
        verbose_name='Картинка'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления (в минутах)',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipe',
        verbose_name='Тэги',
        )
    pub_data = models.DateField()

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.text


class Favorite(models.Model):
    """Модель избранного."""
    pass


class ShoppingCart(models.Model):
    """Модель списка покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shopping_carts",
        verbose_name='Пользователь',
        )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="shopping_carts",
        verbose_name='Рецепт',
        )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shoppingCart_user_recipe'
                )
            ]
