from boards_app.models import Boards
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import BoardsSerializer


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
    serializer_class = BoardsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
