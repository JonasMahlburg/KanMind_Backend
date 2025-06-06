from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import serializers
from tasks_app.models import Tasks, Comment
from boards_app.api.serializers import UserMinimalSerializer


class TasksSerializer(serializers.ModelSerializer):
    """
    Serializer for the Tasks model.

    This serializer handles conversion between Task instances and their JSON representations,
    including assignee and reviewer information, task metadata, and deadlines.

    Fields:
        id (int): Unique identifier of the task.
        board (int): ID of the board this task belongs to.
        title (str): Title of the task.
        description (str): Detailed description of the task.
        status (str): Current status of the task.
        priority (str): Priority level of the task.
        assignee (dict): Serialized user object assigned to the task.
        reviewer (dict): Serialized user object responsible for reviewing the task.
        due_date (date): Deadline for the task.
        comments_count (int): Computed number of comments related to the task.
        assignee_id (int): ID of the assigned user (write-only).
        reviewer_id (int): ID of the reviewer (write-only).
    """

    # assignee_id = serializers.PrimaryKeyRelatedField(
    #     queryset=User.objects.all(),
    #     write_only=True,
    #     source='assignee',
    #     required=True
    # )
    # reviewer_id = serializers.PrimaryKeyRelatedField(
    #     queryset=User.objects.all(),
    #     write_only=True,
    #     source='reviewer',
    #     required=True
    # )
    comments_count = serializers.SerializerMethodField()
    priority = serializers.CharField()
    status = serializers.CharField()
    due_date = serializers.DateField()
    assignee_data = UserMinimalSerializer(source='assignee', read_only=True)
    reviewer_data = UserMinimalSerializer(source='reviewer', read_only=True)

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
            'id',
            'board',
            'title',
            'description',
            'status',
            'priority',
            'assignee_id',         # input: ID
            'reviewer_id',         # input: ID
            'assignee_data',    # output: detailliert
            'reviewer_data',    # output: detailliert
            'due_date',
            'comments_count'
        ]

    # class Meta:
    #     model = Tasks
    #     fields = [
    #         'id', 'board', 'title', 'description', 'status', 'priority',
    #         'assignee', 'reviewer', 'due_date', 'comments_count',
    #         'assignee_id', 'reviewer_id',
    #     ]
    #     extra_kwargs = {
    #         'description': {'required': True},
    #         'status': {'required': True},
    #         'priority': {'required': True},
    #         'due_date': {'required': True},
    #     }

    def get_comments_count(self, obj):
        return obj.comments.count()

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
        fields = ['id', 'task', 'cotend', 'author', 'created_at']
        read_only_fields = ['id', 'created_at', 'task', 'author']

class ReviewerSerializer(serializers.Serializer):
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=True,
        source='reviewer'
    )
