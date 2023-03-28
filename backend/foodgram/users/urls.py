from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewset

app_name = 'users'

v1_router = DefaultRouter()
v1_router.register('users', UserViewset, basename='user')

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt'))
]
