# Generated by Django 4.2 on 2023-04-18 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0013_alter_favorite_recipe_alter_shoppingcart_recipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientinrecipe',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='recipe.ingredient', verbose_name='Ингредиент'),
        ),
    ]