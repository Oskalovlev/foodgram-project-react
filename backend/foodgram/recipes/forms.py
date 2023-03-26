from django import forms

from .models import Recipes


class RecipesForm(forms.ModelForm):

    class Meta:
        model = Recipes
        fields = ('text', 'ingredients', 'image')
        help_text = {
            'text': 'Текст',
            'ingredients': 'Ингридиент',
            'image': 'Картинка'

        }
