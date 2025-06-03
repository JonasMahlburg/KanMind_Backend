from django.contrib.auth import get_user_model
from rest_framework import serializers
from tasks_app.models import Tasks, Comment


class TasksSerializer(serializers.ModelSerializer):
    worked = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=get_user_model().objects.all()
    )
    

    class Meta:
        model = Tasks
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','task', 'text', 'author', 'created_at']
