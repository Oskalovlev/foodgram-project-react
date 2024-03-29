import json

from django.conf import settings
from django.core.management import BaseCommand

from recipe.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        data_path = settings.BASE_DIR
        with open(
                f'{data_path}/static/data/ingredients.json',
                'r',
                encoding='utf-8'
        ) as file:
            data = json.load(file)
            Ingredient.objects.bulk_create(
                Ingredient(**one_ingredient) for one_ingredient in data)
        self.stdout.write(self.style.SUCCESS('Ингредиенты в базе!'))
