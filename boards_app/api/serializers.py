from rest_framework import serializers
from boards_app.models import Boards
from django.contrib.auth.models import User
from tasks_app.models import Tasks



class UserMinimalSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']  # fullname hier ergänzen

    def get_fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


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
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)
    members = UserMinimalSerializer(many=True, read_only=True)
    members_write = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        required=False
    )
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Boards
        fields = ['id', 'title', 'owner_id', 'members_write', 'members', 'tasks']

    def get_tasks(self, obj):
        from tasks_app.api.serializers import TasksSerializerNoBoard
        tasks = obj.tasks.all()
        return TasksSerializerNoBoard(tasks, many=True).data

    def to_representation(self, instance):
        request = self.context.get('request')
        if request and request.method == 'PATCH':
            return {
                'id': instance.id,
                'title': instance.title,
                'owner_data': UserMinimalSerializer(instance.owner).data,
                'members_data': UserMinimalSerializer(instance.members.all(), many=True).data
            }
        return {
            'id': instance.id,
            'title': instance.title,
            'owner_id': instance.owner.id,
            'members': UserMinimalSerializer(instance.members.all(), many=True).data,
            'tasks': self.get_tasks(instance)
        }

    def update(self, instance, validated_data):
        members_data = validated_data.pop('members_write', None)
        instance = super().update(instance, validated_data)
        if members_data is not None:
            instance.members.set(members_data)
        return instance