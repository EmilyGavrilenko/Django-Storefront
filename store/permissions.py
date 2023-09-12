from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS: # GET, HEAD, OPTIONS
            return True
        return bool(request.user and request.user.is_staff)