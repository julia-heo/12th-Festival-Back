from rest_framework import serializers
from .models import Booth, Menu, Comment, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'booth', 'user', 'content', 'created_at', 'updated_at']
        read_only_fields= ('booth', 'user', )