from rest_framework import serializers

from .models import *
from accounts.models import User


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id','booth', 'menu', 'price', 'is_soldout','like','img']


class BoothListSerializer(serializers.ModelSerializer):
    day = serializers.StringRelatedField(many=True, read_only=True)
    is_liked = serializers.BooleanField(default=False)
    category = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Booth

        fields = ['id', 'user', 'day', 'college', 'category', 'name', 
                  'number', 'thumnail', 'opened', 'times','is_liked', 'performance']
        read_only_fields= ('thumnail', )



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    mine=serializers.BooleanField(default=False)
    manager=serializers.BooleanField(default=False)

    class Meta:
        model = Comment
        fields = ['id', 'booth', 'user', 'content', 'created_at', 'updated_at']
        read_only_fields= ('booth', 'user', )


class BoothDetailSerializer(serializers.ModelSerializer):
    day = serializers.StringRelatedField(many=True, read_only=True)
    category = serializers.StringRelatedField(many=True, read_only=True)
    menus = MenuSerializer(read_only=True, many=True)
    is_liked = serializers.BooleanField(default=False)
    comments = CommentSerializer(many=True, read_only=True)
    like_num=serializers.IntegerField()

    class Meta:
        model = Booth
        fields = ['id', 'user', 'day', 'college', 'category', 'name', 
                  'number', 'thumnail', 'opened', 'times',
                  'description','menus', 'is_liked', 'created_at', 'updated_at',
                    'comments', 'contact', 'realtime', 'performance']