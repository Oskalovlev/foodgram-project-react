from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewset

app_name = 'user'

router = DefaultRouter()

router.register('users', CustomUserViewset, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
