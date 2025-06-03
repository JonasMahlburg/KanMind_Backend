from rest_framework import serializers
from boards_app.models import Boards
from tasks_app.models import Tasks

class BoardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boards
        fields = ['id','title', 'member_count', 'tasks_count', 'tasks_to_do_count']
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
    
    member_count = serializers.SerializerMethodField()
    tasks_count = serializers.SerializerMethodField()

    def get_member_count(self, obj):
        return obj.members.count()  # 'members' ist das ManyToManyField

    def get_tasks_count(self, obj):
        return obj.tasks.count()  # 'tasks' ist der related_name vom Task-Model
    
