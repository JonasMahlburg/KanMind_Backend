from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from tasks_app.models import Tasks, Comment
from rest_framework import viewsets
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated
from .serializers import TasksSerializer, CommentSerializer
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
        
  

class TasksAssignedToMeAsReviewerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = TasksSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tasks.objects.filter(reviewer=self.request.user)

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


# Neue View zum Zuweisen eines Reviewers zu einer Task
class ReviewerAssignView(GenericAPIView):
    serializer_class = TasksSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, task_pk):
        """
        Weist einer Task einen Reviewer zu.
        Erwartet: { "reviewer_id": <int> }
        """
        task = get_object_or_404(Tasks, pk=task_pk)
        reviewer_id = request.data.get("reviewer_id")
        if reviewer_id is None:
            return Response({"detail": "reviewer_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        # Reviewer-Feld setzen
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            reviewer = User.objects.get(pk=reviewer_id)
        except User.DoesNotExist:
            return Response({"detail": "Reviewer not found."}, status=status.HTTP_404_NOT_FOUND)
        task.reviewer = reviewer
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)