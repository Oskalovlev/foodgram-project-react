from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, ShoppingCartViewSet


v1_router = DefaultRouter()

v1_router.register('recipes', RecipeViewSet, basename='recipes')
v1_router.register('ingredients', IngredientViewSet, basename='ingredients')
v1_router.register(
    r'recipes/(?P<recipes_id>\d+)/shopping_cart/',
    ShoppingCartViewSet,
    basename='shopping_cart'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
