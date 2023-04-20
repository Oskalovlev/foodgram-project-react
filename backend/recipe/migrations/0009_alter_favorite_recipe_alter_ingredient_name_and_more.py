# Generated by Django 4.2 on 2023-04-14 15:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0008_remove_recipe_ingredients_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='recipe.recipe', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=200, unique=True, validators=[django.core.validators.RegexValidator(inverse_match=True, regex='^[\\w$%^&#:;!]+\\Z')], verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=200, unique=True, validators=[django.core.validators.RegexValidator(inverse_match=True, regex='^[\\w$%^&#:;!]+\\Z')], verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='recipe.recipe', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(default='#ffffff', max_length=7, unique=True, validators=[django.core.validators.RegexValidator(regex='^#([0-9a-fA-F]{3,6})$')], verbose_name='Цвет'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=200, unique=True, validators=[django.core.validators.RegexValidator(inverse_match=True, regex='^[\\w$%^&#:;!]+\\Z')], verbose_name='Название'),
        ),
    ]