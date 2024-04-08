from rest_framework import serializers
from .models import Notice

class NoticeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Notice
        fields = ['id','user','title', 'content', 'created_at', 'updated_at']
        read_only = ('user')