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
        return obj.comments.count()
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.method == 'PATCH':
            data.pop('board', None)  # Board entfernen
            data.pop('comments_count', None)  # comments_count entfernen
        return data
    
    
class CommentSerializer(serializers.ModelSerializer):
    content = serializers.CharField(source='text')
    author = serializers.CharField(source='author.get_full_name', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']

        

class ReviewerSerializer(serializers.Serializer):
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=True,
        source='reviewer'
    )

class TasksSerializerNoBoard(serializers.ModelSerializer):
    description = serializers.CharField()
    assignee = UserMinimalSerializer(read_only=True)
    reviewer = UserMinimalSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Tasks
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'assignee',
            'reviewer',
            'due_date',
            'comments_count',
        ]

    def get_comments_count(self, obj):
        return obj.comments.count()