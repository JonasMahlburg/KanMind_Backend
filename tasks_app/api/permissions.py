from rest_framework.permissions import BasePermission, SAFE_METHODS
        
class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to allow only the author of an object or a superuser to edit or delete it.
    Safe methods (like GET, HEAD, OPTIONS) are allowed for everyone.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method == "DELETE":
            return bool(request.user and (request.user.is_superuser or request.user == obj.author))
        else:
            return bool(request.user and request.user == obj.author)