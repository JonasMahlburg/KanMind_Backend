from django.contrib.auth import get_user_model
from rest_framework import serializers
from tasks_app.models import Tasks, Comment


class TasksSerializer(serializers.ModelSerializer):
    """
    Serializer for the Tasks model.

    This serializer handles conversion between Task instances and their JSON representations,
    including user assignments, deadlines, and ownership.

    Fields:
        id (int): Unique identifier of the task.
        title (str): Title of the task.
        content (str): Description or content of the task.
        board (int): ID of the board this task belongs to.
        owner (int): ID of the user who created the task.
        worked (list[int]): List of user IDs assigned to the task.
        deadline (date): Optional deadline for completing the task.
    """
    worked = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=get_user_model().objects.all()
    )
    deadline = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = Tasks
        fields = ['id', 'title', 'content', 'board', 'owner', 'worked', 'deadline']

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.

    This serializer converts Comment instances to and from JSON,
    allowing interaction with comments related to tasks.

    Fields:
        id (int): Unique identifier of the comment.
        task (int): ID of the task the comment is associated with.
        text (str): Content of the comment.
        author (int): ID of the user who wrote the comment.
        created_at (datetime): Timestamp of when the comment was created.
    """
    class Meta:
        model = Comment
        fields = ['id','task', 'text', 'author', 'created_at']
