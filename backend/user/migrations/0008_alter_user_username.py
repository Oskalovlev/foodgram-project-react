# Generated by Django 4.2 on 2023-04-24 07:00

import django.core.validators
from django.db import migrations, models
import user.validators


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_user_first_name_alter_user_last_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator(regex='^[a-zA-Z0-9]+$'), user.validators.username_validator], verbose_name='Пользователь'),
        ),
    ]
