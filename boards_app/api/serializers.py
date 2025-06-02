from rest_framework import serializers
from boards_app.models import Boards

class BoardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boards
        fields = ['title', 'member_count']