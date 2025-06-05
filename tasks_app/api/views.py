from tasks_app.models import Tasks, Comment
from rest_framework import viewsets
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated
from .serilaizers import TasksSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly




class TasksViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing tasks.

    Allows authenticated users to create, retrieve, update, and delete tasks.
    Read-only access is granted to unauthenticated users.

    Methods:
        perform_create(serializer): Sets the task owner to the current user.
    """
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing comments related to a specific task.

    Filters comments based on the parent task ID provided in the URL.
    Allows read and write operations based on user permissions.

    Methods:
        get_queryset(): Returns all comments related to the given task.
        perform_create(serializer): Assigns the current user as the comment author 
            and links the comment to the task.
    """
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
    """
    ViewSet for listing tasks assigned to the current user.

    Only allows authenticated users to retrieve tasks they are working on.

    Methods:
        get_queryset(): Returns tasks where the current user is listed in the 'worked' field.
    """
    serializer_class = TasksSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tasks.objects.filter(assignee=self.request.user)

class TasksInReviewViewset(mixins.ListModelMixin, GenericViewSet):
    """
    ViewSet for listing tasks with status 'review'.

    Only accessible by authenticated users.

    Methods:
        get_queryset(): Returns tasks with status set to 'review'.
    """
    serializer_class = TasksSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tasks.objects.filter(status="reviewing")
    
class TasksHighPrioViewset(mixins.ListModelMixin, GenericViewSet):
    """
    ViewSet for listing tasks with high priority.

    Only accessible by authenticated users.

    Methods:
        get_queryset(): Returns tasks where priority is set to 'high'.
    """
    serializer_class = TasksSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tasks.objects.filter(priority="high")