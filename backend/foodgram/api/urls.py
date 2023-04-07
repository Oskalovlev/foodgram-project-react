from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TagViewSet, IngredientViewSet, RecipeViewSet

app_name = 'api'

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tag')
router.register('recipes', RecipeViewSet, basename='recipe')
router.register('ingredients', IngredientViewSet, basename='ingredient')

urlpatterns = [
    path('', include(router.urls)),
    path('api/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
