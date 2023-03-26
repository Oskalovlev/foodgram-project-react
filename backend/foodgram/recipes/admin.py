from django.contrib import admin

from .models import Ingredient, Recipe, Tag


class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'cooking_time',
                    'id')
    search_fields = ('name', 'author', 'tags')
    list_filter = ('name', 'author', 'tags')
    empty_value_display = '--empty--'


admin.site.register(Recipe, RecipesAdmin)
admin.site.register(Ingredient)
admin.site.register(Tag)
