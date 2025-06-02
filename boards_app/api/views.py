from boards_app.models import Boards
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from .serializers import BoardsSerializer


class BoardsViewSet(viewsets.ModelViewSet):
    queryset = Boards.objects.all()
    serializer_class = BoardsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
