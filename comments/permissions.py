from rest_framework import permissions


class IsOwnerCommentOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS or
            obj and obj.author.pk == request.user.pk
        )
