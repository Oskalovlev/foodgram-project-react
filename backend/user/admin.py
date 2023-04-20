from django.contrib import admin

from .models import User, Subscription


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'count_subscribers',
        'count_recipes',
    )
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    read_only_fields = ('count_subscribers', 'count_recipes')
    empty_value_display = '--empty--'

    @admin.display(description='Количество подписчиков')
    def count_subscribers(self, obj):
        """Получаем количество подписчиков."""
        return obj.subscriber.count()

    @admin.display(description='Количество рецептов')
    def count_recipes(self, obj):
        """Получаем количество подписчиков."""
        return obj.recipes.count()


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', )
    empty_value_display = '--empty--'
