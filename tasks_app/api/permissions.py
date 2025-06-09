from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import NotAuthenticated, PermissionDenied

class IsBoardMemberOrReadOnly(BasePermission):
    """
    Custom permission to allow only members of a task's board to edit or delete the task.
    Safe methods (like GET, HEAD, OPTIONS) are allowed for everyone.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        if not user or not user.is_authenticated:
            raise NotAuthenticated(detail="Unauthorized. The user must be logged in.")

        if request.method == "DELETE":
            if user == obj.author or user == obj.board.owner:
                return True
            raise PermissionDenied(detail="Forbidden. Only the task author or the board owner can delete the task.")

        if user not in obj.board.members.all():
            raise PermissionDenied(detail="Forbidden. The user must be a member of the board to which the task belongs.")

        # If all checks pass, permission is granted
        return True