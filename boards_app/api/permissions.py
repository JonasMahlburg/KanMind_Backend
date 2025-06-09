from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied, NotAuthenticated

class BoardAccessPermission(BasePermission):
    """
    Custom permission for Board access control:
    - Authenticated users can retrieve/update/modify boards if they are the owner or a member.
    - Only the owner can delete the board.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        if not user.is_authenticated:
            raise NotAuthenticated(detail="Unauthorized. The user must be logged in to access this resource.")

        if view.action in ['retrieve', 'update', 'partial_update']:
            if user == obj.owner or user in obj.members.all():
                return True
            raise PermissionDenied(detail="Forbidden. The user must be either a board member or the owner to access this resource.")

        if view.action == 'destroy':
            if user == obj.owner:
                return True
            raise PermissionDenied(detail="Forbidden. Only the board owner can delete this board.")

        return True