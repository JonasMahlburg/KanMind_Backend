from tasks_app.models import Tasks, Comment
from rest_framework import viewsets
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated
from .serilaizers import TasksSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly




class TasksViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        task_id = self.kwargs.get('task_pk')
        return Comment.objects.filter(task__id=task_id)

    def perform_create(self, serializer):
        task_id = self.kwargs.get('task_pk')
        task = Tasks.objects.get(id=task_id)
        serializer.save(author=self.request.user, task=task)
        
  


class MyAssignedTasksViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = TasksSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tasks.objects.filter(assigned_to=self.request.user)

class TasksInReviewViewset(mixins.ListModelMixin, GenericViewSet):
    serializer_class = TasksSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tasks.objects.filter(status="review")