from rest_framework import permissions


# class IsReadOnly(permissions.BasePermission):
#     """Доступ только для чтения."""

#     def has_permission(self, request, view):
#         return (request.method in permissions.SAFE_METHODS
#                 or request.user.is_authenticated)

#     def has_object_permission(self, request, view, obj):
#         return request.method in permissions.SAFE_METHODS


class IsAuthor(permissions.BasePermission):
    """Доступ для автора."""

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


# class IsAdmin(permissions.BasePermission):
#     """Доступ для администратора."""

#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.is_admin
