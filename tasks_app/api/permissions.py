from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import NotAuthenticated, PermissionDenied


class IsBoardMemberOrReadOnly(BasePermission):
    """
    Permission class to control task access based on board membership.

    - Safe methods (GET, HEAD, OPTIONS) are always allowed.
    - Only the task author or board owner can delete a task.
    - Only board members can update a task.
    """

    def has_object_permission(self, request, view, obj):
        """
        Determine if the user has permission to perform the action on the task object.

        Args:
            request: The HTTP request object.
            view: The view object.
            obj: The task instance being accessed.

        Returns:
            bool: True if access is permitted, otherwise raises an exception.
        """
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