from tasks_app.models import Tasks
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serilaizers import TasksSerializer

class tasksViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [AllowAny]