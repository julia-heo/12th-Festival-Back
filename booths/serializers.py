from rest_framework import serializers

from .models import *
from accounts.models import User


class MenuSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    class Meta:
        model = Menu
        fields = ['id', 'menu', 'price', 'is_soldout','is_liked','img']
    def get_is_liked(self,obj):   
        user = self.context.get('user') 
        return obj.like.filter(pk=user).exists()
    def get_price(self,obj):   
        return str(obj.price)+"원"
    
class BoothListSerializer(serializers.ModelSerializer):
    is_liked = serializers.BooleanField(default=False)
    info = serializers.SerializerMethodField()
    class Meta:
        model=Booth
        fields=['id', 'name', 'info','thumnail','opened','is_liked']
    
    def get_info(self, obj):
        return obj.college+" "+obj.number


class CommentSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    mine = serializers.SerializerMethodField()
    manager = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id', 'nickname','content', 'created_at', 'mine','manager']
        read_only_fields= ('booth', 'user', )
    def get_nickname(self, obj):
        return obj.user.nickname
    def get_mine(self, obj):
        user = self.context.get('user')
        return obj.user.id==user
    def get_manager(self, obj):
        return obj.user == obj.booth.user
    def get_created_at(self, obj):
        return obj.created_at.strftime("%-m월 %-d일 %-H시 %-M분")

    
class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','booth', 'user','content', 'created_at', 'updated_at']



class BoothDetailSerializer(serializers.ModelSerializer):
    day = serializers.StringRelatedField(many=True, read_only=True)
    updated_at = serializers.SerializerMethodField()
    menus = serializers.SerializerMethodField()
    is_liked = serializers.BooleanField(default=False)
    comments = serializers.SerializerMethodField()
    like_num=serializers.SerializerMethodField()

    class Meta:
        model = Booth
        fields = ['id', 'user', 'day', 'college', 'category', 'name', 
                  'number', 'thumnail', 'opened',
                  'description','is_liked', 'like_num', 'realtime', 'updated_at',
                 'contact', 'performance','menus','comments']
    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%-m월 %-d일 %-H시 %-M분")
    def get_like_num(self, obj):
        return obj.like.count()
    def get_menus(self, obj):
        menus = obj.menus.all()
        menus_serializer = MenuSerializer(menus, many=True, context=self.context)
        return menus_serializer.data
    def get_comments(self, obj):
        comments = obj.comments.all()
        comments_serializer = CommentSerializer(comments, many=True, context=self.context)
        return comments_serializer.data

        

class MenuListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    is_liked = serializers.BooleanField(default=False)
    booth_id = serializers.SerializerMethodField()
    info = serializers.SerializerMethodField()
    thumnail = serializers.SerializerMethodField()
    opened = serializers.SerializerMethodField()
    class Meta:
        model=Menu
        fields=['id', 'name',"booth_id", 'info','thumnail','opened','is_liked']
    
    def get_name(self,obj):
        return obj.menu
    def get_booth_id(self,obj):
        return obj.booth.id
    def get_info(self, obj):
        return str(obj.price)+"원"
    def get_thumnail(self, obj):
        return obj.img
    def get_opened(self, obj):
        return not obj.is_soldout