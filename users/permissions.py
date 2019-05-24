from rest_framework import permissions


class IsAccountOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the owner of a user account to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user


class IsSuperUser(permissions.BasePermission):
    """
    Custom permission to only allow the database administrator
    (`is_superuser == True`) to do something.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser


class IsConfirmedOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow a confirmed user
    (`is_confirmed == True`) to do something.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_confirmed


class IsConfirmed(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_confirmed
