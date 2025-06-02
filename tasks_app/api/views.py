from tasks_app.models import Tasks
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from .serilaizers import TasksSerializer

class TasksViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# class TasksDetailViewSet(viewsets.ModelViewSet):
#     queryset = Tasks.objects.all()
#     serializer_class = TasksSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]


