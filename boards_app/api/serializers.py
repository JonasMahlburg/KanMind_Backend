from rest_framework import serializers
from boards_app.models import Boards

class BoardsSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    owner_id = serializers.IntegerField(source='owner.id')

    class Meta:
        model = Boards
        fields = [
            'id',
            'title',
            'member_count',
            'ticket_count',
            'tasks_to_do_count',
            'tasks_high_prio_count',
            'owner_id'
        ]

    def get_member_count(self, obj):
        return obj.members.count()

    def get_ticket_count(self, obj):
        return obj.tasks_to_do.all().count()  # oder obj.tasks.count(), je nach Logik

    def get_tasks_to_do_count(self, obj):
        return obj.tasks_to_do.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks_to_do.filter(prio='high')
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
