from rest_framework import permissions


class IsCurrentUserAuthenticated(permissions.BasePermission):
    lookup_url_kwarg = 'user_id'

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated
            and self.lookup_url_kwarg in view.kwargs
            and int(view.kwargs[self.lookup_url_kwarg]) == request.user.pk
        )
