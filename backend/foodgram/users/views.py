from django.shortcuts import get_object_or_404
from rest_framework import generics, status, views, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .pagination import LimitPageNumberPagination


class UserViewset(viewsets.ModelViewSet):
    pass
    # pagination_class = LimitPageNumberPagination
