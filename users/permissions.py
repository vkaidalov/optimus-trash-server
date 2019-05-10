from rest_framework import permissions


class IsAccountOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the owner of a user account to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user
