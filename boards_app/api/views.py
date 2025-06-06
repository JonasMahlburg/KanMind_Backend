from boards_app.models import Boards
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import BoardsSerializer, BoardsDetailSerializer
from rest_framework.generics import RetrieveAPIView



class BoardsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows boards to be viewed, created, updated, or deleted.

    This viewset provides full CRUD functionality for the Boards model.
    It uses the BoardsSerializer for serialization and enforces authentication
    for modifying data, while allowing read-only access to unauthenticated users.

    Attributes:
        queryset (QuerySet): All board instances from the database.
        serializer_class (Serializer): The serializer class used for board instances.
        permission_classes (list): List of permission classes that control access.
    """
    queryset = Boards.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BoardsDetailSerializer
        return BoardsSerializer


class BoardsDetailView(RetrieveAPIView):
    """
    API view to retrieve detailed information of a single board,
    including members and tasks with nested related data.
    """
    queryset = Boards.objects.all()
    serializer_class = BoardsDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            return BoardsDetailSerializer
        return BoardsSerializer