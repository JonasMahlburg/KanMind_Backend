from rest_framework import serializers
from boards_app.models import Boards
from django.contrib.auth.models import User
from tasks_app.models import Tasks



class UserMinimalSerializer(serializers.ModelSerializer):
    """
    Minimal serializer for User model.

    Provides a compact representation of a user, including ID, email,
    and a computed full name combining first and last names.

    Fields:
        id (int): Unique identifier of the user.
        email (str): Email address of the user.
        fullname (str): Concatenation of first and last names.
    """
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        """
        Return the full name of the user by combining first and last name.

        Args:
            obj (User): The user instance.

        Returns:
            str: The full name of the user.
        """
        full_name = f"{obj.first_name} {obj.last_name}".strip()
        return full_name


class BoardsSerializer(serializers.ModelSerializer):
    """
    Serializer for the Boards model.

    This serializer provides computed fields to display metadata about a board,
    such as the number of members, tickets, tasks to do, and high-priority tasks.
    It also includes the owner's ID explicitly.

    Fields:
        id (int): Unique identifier of the board.
        title (str): Title of the board.
        member_count (int): Total number of users assigned to the board.
        ticket_count (int): Total number of tasks related to the board.
        tasks_to_do_count (int): Count of tasks with status 'to-do'.
        tasks_high_prio_count (int): Count of tasks with priority 'high'.
        owner_id (int): ID of the user who owns the board.

    Methods:
        get_member_count(obj): Returns the number of members associated with the board.
        get_ticket_count(obj): Returns the number of tasks related to the board.
        get_tasks_to_do_count(obj): Returns the number of tasks with status 'to-do'.
        get_tasks_high_prio_count(obj): Returns the number of tasks with priority 'high'.
        perform_create(serializer): Sets the owner of the board to the current request user.
    """
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()


    # WRITE: Accepts member IDs
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True
    )

    class Meta:
        model = Boards
        fields = [
            'id',
            'title',
            'member_count',
            'ticket_count',
            'tasks_to_do_count',
            'tasks_high_prio_count',
            'owner_id',
            'members',    
        ]



    def get_member_count(self, obj):
        """
        Return the number of members associated with the board.

        Args:
            obj (Boards): The board instance.

        Returns:
            int: Number of users linked as members.
        """
        return obj.members.count()

    def get_ticket_count(self, obj):
        """
        Return the number of tasks assigned to the board.

        Args:
            obj (Boards): The board instance.

        Returns:
            int: Number of related tasks.
        """
        return obj.tasks.count()

    def get_tasks(self, obj):
        """
        Return serialized list of tasks with status 'to-do' for the board.

        Args:
            obj (Boards): The board instance.

        Returns:
            list: Serialized data of tasks with status 'to-do'.
        """
        from tasks_app.api.serializers import TasksSerializer
        tasks = obj.tasks.filter(status='to-do')
        return TasksSerializer(tasks, many=True).data

    def get_tasks_high_prio_count(self, obj):
        """
        Return the number of tasks with high priority.

        Args:
            obj (Boards): The board instance.

        Returns:
            int: Count of tasks with priority set to 'high'.
        """
        return obj.tasks.filter(priority='high').count()
    
    def get_tasks_to_do_count(self, obj):
        """
        Return the number of tasks with status to-do.

        Args:
            obj (Boards): The board instance.

        Returns:
            int: Count of tasks with priority set to 'high'.
        """
        return obj.tasks.filter(status='to-do').count()


class BoardsDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for the Boards model.

    Includes basic board information, a list of member users,
    and a list of all associated tasks with full task detail.
    """
    owner_data = UserMinimalSerializer(source='owner', read_only=True)
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        required=False
    )
    members_data = UserMinimalSerializer(source='members', many=True, read_only=True)
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Boards
        fields = ['id', 'title', 'owner_data', 'members', 'members_data', 'tasks']

    def get_tasks(self, obj):
        view = self.context.get('view')
        if view and view.action in ['update', 'partial_update']:
            return None
        from tasks_app.api.serializers import TasksSerializer
        return TasksSerializer(obj.tasks.all(), many=True).data

    def update(self, instance, validated_data):
        members_data = validated_data.pop('members', None)
        instance = super().update(instance, validated_data)
        if members_data is not None:
            instance.members.set(members_data)
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        view = self.context.get('view')
        if view and view.action in ['update', 'partial_update']:
            data.pop('tasks', None)
        return data
