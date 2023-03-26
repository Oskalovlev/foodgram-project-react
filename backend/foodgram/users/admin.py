from django.contrib import admin

from .models import Subscriber, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'id')
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    empty_value_display = '--empty--'


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')
    search_fields = ('user', 'following')
    list_filter = ('user', )
    empty_value_display = '--empty--'


admin.site.register(User, UserAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
