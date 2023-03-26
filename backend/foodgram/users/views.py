from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .pagination import LimitPageNumberPagination


class UserViewset(viewsets.UserViewSet):
    pagination_class = LimitPageNumberPagination
    
