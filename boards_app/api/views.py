from boards_app.models import Boards
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import BoardsSerializer, BoardsDetailSerializer
from rest_framework.generics import RetrieveAPIView
from boards_app.api.permissions import BoardAccessPermission



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