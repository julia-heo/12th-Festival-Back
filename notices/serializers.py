from rest_framework import serializers
from .models import *

class NoticeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Notice
        fields = ['id','user','title', 'content', 'created_at', 'updated_at']
        read_only = ('user')

class EventListSerializer(serializers.ModelSerializer):
    day = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model=Event
        fields = ['user','name','day','place', 'summary', 'thumnail']
    
class EventDetailSerializer(serializers.ModelSerializer):
    day = serializers.StringRelatedField(many=True, read_only=True)
    updated_at = serializers.SerializerMethodField()
    class Meta:
        model=Event
        fields = ['user','name', 'place', 'summary', 'thumnail', 'updated_at','day','opened',
                'description','contact','realtime']
    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%-m월 %-d일 %-H시 %-M분")
    