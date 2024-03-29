# Generated by Django 4.2 on 2023-04-18 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0012_alter_favorite_recipe_alter_shoppingcart_recipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='recipe.recipe', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart', to='recipe.recipe', verbose_name='Рецепт'),
        ),
    ]
