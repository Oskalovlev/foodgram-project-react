from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from user.models import User


class NameModel(models.Model):
    """Абстрактная модель представления <названия>."""

    name = models.CharField(
        'Название',
        max_length=settings.DATA_LENGTH_RECIPE,
        unique=True,
        validators=[RegexValidator(
            regex=settings.CHARACTER_VALIDATOR,
            inverse_match=True,)]
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Tag(NameModel):
    """Модель тэга."""

    color = models.CharField(
        'Цвет',
        max_length=settings.COLOR_LENGTH,
        unique=True,
        validators=[
            RegexValidator(regex=r'^#([0-9a-fA-F]{3,6})$')
        ],
        default="#ffffff",
    )
    slug = models.SlugField(
        'Slug',
        unique=True,
        max_length=settings.DATA_LENGTH_RECIPE,
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(NameModel):
    """Модель ингредиента."""

    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=settings.DATA_LENGTH_RECIPE,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit',),
                name='unique_ingredient',
            ),
        )

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Recipe(NameModel):
    """Модель рецепта."""

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Автор'
    )
    text = models.TextField('Описание')
    image = models.ImageField(
        'Картинка',
        upload_to='recipe/',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления (в минутах)',
        validators=[MinValueValidator(1)],
        default=1
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
    )
    pub_date = models.DateField(
        'Дата публикации',
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        default_related_name = 'recipes'

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    """Модель ингредиента в рецепте."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='ingredients',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='+'
    )
    amount = models.PositiveSmallIntegerField(
        'Кол-во',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        ordering = ('recipe',)
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        constraints = (
            models.UniqueConstraint(
                fields=('ingredient', 'recipe',),
                name='unique_ingredient_recipe',
            ),
        )

    def __str__(self):
        return f'{self.ingredient} {self.recipe} {self.amount}'


class Favorite(models.Model):
    """Модель избранного."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранные'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_favorite',
            ),
        )

    def __str__(self):
        return f'{self.user} {self.recipe}'


class ShoppingCart(models.Model):
    """Модель списка покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_shopping',
            ),
        )

    def __str__(self):
        return f'{self.user} {self.recipe}'
