# Generated by Django 4.2 on 2023-04-23 10:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0021_alter_ingredient_name_alter_recipe_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(regex='^[а-яА-ЯёЁa-zA-Z0-9]+$')], verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(regex='^[а-яА-ЯёЁa-zA-Z0-9]+$')], verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(regex='^[а-яА-ЯёЁa-zA-Z0-9]+$')], verbose_name='Название'),
        ),
    ]
