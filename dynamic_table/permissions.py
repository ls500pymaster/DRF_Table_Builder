from rest_framework.permissions import BasePermission


class DynamicTablePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('POST',):
            return request.user.is_authenticated and request.user.is_staff
        return request.method in ('GET',)  # Allow read-only access for all users
