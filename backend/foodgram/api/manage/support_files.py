# import csv
from base64 import b64decode

# from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from rest_framework import serializers

# from recipe.models import Ingredient


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)

    def to_representation(self, file):
        return '/media/' + super().to_representation(file)


# class CSVIngredients(BaseCommand):

#     def handle(self, *args, **kwargs):
#         with open('./data/ingredients.csv', encoding='utf-8') as r_file:
#             file_reader = csv.reader(r_file)
#             next(file_reader)
#             for row in file_reader:
#                 Ingredient.objects.get_or_create(
#                     name=row[0],
#                     measurement_unit=row[1],
#                 )
