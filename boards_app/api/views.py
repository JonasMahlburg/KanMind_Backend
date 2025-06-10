from boards_app.models import Boards
from rest_framework import viewsets
from rest_framework.permissions import BasePermission
from .serializers import BoardsSerializer, BoardsDetailSerializer
from rest_framework.exceptions import NotAuthenticated, PermissionDenied


# Permission class to control access to Board instances.
class BoardAccessPermission(BasePermission):
    """
    Permission class to control access to Board instances.

    - Only authenticated users can access any board-related endpoint.
    - Users can retrieve/update if they are the owner or a member.
    - Only owners can delete.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated(detail="Authentication required to access boards.")
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        if request.method in ['GET', 'PUT', 'PATCH']:
            if obj.owner == user or user in obj.members.all():
                return True

        if request.method == 'DELETE':
            if obj.owner == user:
                return True

        raise PermissionDenied("Forbidden. You do not have permission to perform this action.")


class BoardsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Boards.

    Provides CRUD operations for the Boards model with appropriate
    serializer selection based on the action.

    Behavior:
        - Uses `BoardsDetailSerializer` for `retrieve` and `partial_update` actions
          to provide detailed serialization.
        - Uses `BoardsSerializer` for other actions, such as list and create.
        - Automatically assigns the currently authenticated user as the owner
          when creating a new board.

    Permissions:
        - By default, allows any read-only access.
        - Write operations require authentication (handled elsewhere if needed).
    """

    queryset = Boards.objects.all()
    permission_classes = [BoardAccessPermission]

    def get_serializer_class(self):
        """
        Returns the serializer class to use for the current action.

        Returns:
            Serializer class for the given action.
        """
        if self.action in ['retrieve', 'partial_update']:
            return BoardsDetailSerializer
        return BoardsSerializer

    def perform_create(self, serializer):
        """
        Handles creation of a new Board instance.

        Automatically sets the owner field to the currently authenticated user.

        Args:
            serializer (Serializer): The serializer instance with validated data.
        """
        serializer.save(owner=self.request.user)