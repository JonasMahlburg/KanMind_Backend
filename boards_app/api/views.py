from boards_app.models import Boards
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import BoardsSerializer, BoardsDetailSerializer
from rest_framework.generics import RetrieveAPIView



class BoardsViewSet(viewsets.ModelViewSet):
    queryset = Boards.objects.all()

    def get_serializer_class(self):
        if self.action in ['retrieve', 'partial_update']:
            return BoardsDetailSerializer
        return BoardsSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)