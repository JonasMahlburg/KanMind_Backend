from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import serializers
from tasks_app.models import Tasks, Comment
from boards_app.api.serializers import UserMinimalSerializer


class TasksSerializer(serializers.ModelSerializer):
    """
    Serializer for the Tasks model.

    Handles serialization and deserialization of Task instances,
    including assignee and reviewer details, task metadata, and deadlines.

    Fields:
        id (int): Unique identifier of the task.
        board (int): ID of the board the task belongs to.
        title (str): Title of the task.
        description (str): Detailed description of the task.
        status (str): Current status of the task.
        priority (str): Priority level of the task.
        assignee (UserMinimalSerializer): Serialized assignee user data (read-only).
        reviewer (UserMinimalSerializer): Serialized reviewer user data (read-only).
        assignee_id (int): ID of the assigned user (write-only).
        reviewer_id (int): ID of the reviewer (write-only).
        due_date (date): Deadline for the task.
        comments_count (int): Number of comments associated with the task (read-only).
    """

    comments_count = serializers.SerializerMethodField()
    priority = serializers.CharField()
    status = serializers.CharField()
    due_date = serializers.DateField()
    assignee = UserMinimalSerializer(read_only=True)
    reviewer = UserMinimalSerializer(read_only=True)

    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='assignee',
        write_only=True,
        required=True,
    )

    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='reviewer',
        write_only=True,
        required=True,
    )

    class Meta:
        model = Tasks
        fields = [
            'id', 'board', 'title', 'description', 'status', 'priority',
            'assignee', 'reviewer',
            'assignee_id', 'reviewer_id',
            'due_date', 'comments_count'
        ]
        extra_kwargs = {
            'title': {'required': True},
            'description': {'required': True},
            'status': {'required': True},
            'priority': {'required': True},
            'due_date': {'required': True},
            'board': {'required': True},
        }

    def get_comments_count(self, obj):
        """
        Returns the number of comments related to the task.

        Args:
            obj (Tasks): The task instance.

        Returns:
            int: The count of related comments.
        """
        return obj.comments.count()

    def to_representation(self, instance):
        """
        Customize the serialized representation of the task.

        Removes 'board' and 'comments_count' fields from the response
        if the request method is PATCH.

        Args:
            instance (Tasks): The task instance.

        Returns:
            dict: Serialized data of the task.
        """
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.method == 'PATCH':
            data.pop('board', None)
            data.pop('comments_count', None)
        return data


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.

    Fields:
        id (int): Unique identifier of the comment.
        created_at (datetime): Timestamp of when the comment was created.
        author (str): Full name of the comment author (read-only).
        content (str): Text content of the comment.
    """

    content = serializers.CharField(source='text')
    author = serializers.CharField(source='author.get_full_name', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']


class ReviewerSerializer(serializers.Serializer):
    """
    Serializer to validate the reviewer field for a task.

    Fields:
        reviewer_id (PrimaryKeyRelatedField): ID of the user assigned as reviewer.
            This field is required.

    Source:
        reviewer: Corresponds to the 'reviewer' field in the Tasks model.
    """

    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=True,
        source='reviewer'
    )


class TasksSerializerNoBoard(serializers.ModelSerializer):
    """
    Serializer for tasks excluding board information.

    Used when task data is required without including the related board.

    Fields:
        id (int): Unique identifier of the task.
        title (str): Title of the task.
        description (str): Detailed description.
        status (str): Status of the task.
        priority (str): Priority level.
        assignee (UserMinimalSerializer): Serialized assignee data (read-only).
        reviewer (UserMinimalSerializer): Serialized reviewer data (read-only).
        due_date (date): Deadline for the task.
        comments_count (int): Number of comments (read-only).
    """

    description = serializers.CharField()
    assignee = UserMinimalSerializer(read_only=True)
    reviewer = UserMinimalSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Tasks
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'assignee', 'reviewer', 'due_date', 'comments_count',
        ]

    def get_comments_count(self, obj):
        """
        Returns the number of comments related to the task.

        Args:
            obj (Tasks): The task instance.

        Returns:
            int: Count of related comments.
        """
        return obj.comments.count()