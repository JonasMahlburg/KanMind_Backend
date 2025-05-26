from tasks_app.models import Tasks
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from tasks_app.api.serilaizers import TasksSerializer

class tasksViewSet(viewsets.ViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [AllowAny]