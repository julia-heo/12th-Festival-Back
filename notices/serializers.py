from rest_framework import serializers
from .models import *
from booths.models import *
from django.utils import timezone

class NoticeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Notice
        fields = ['id','user','title', 'content', 'created_at', 'updated_at']
        read_only = ('user')

class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = ['id', 'day', 'date', 'start_time', 'end_time']

class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields = ['id','user','name','place', 'opened','type', 'thumnail']
    
class EventDetailSerializer(serializers.ModelSerializer):
    days = DaySerializer(many=True, read_only=True)
    updated_at = serializers.SerializerMethodField()
    class Meta:
        model=Event
        fields = ['id','user','name', 'place','thumnail', 'opened','updated_at','days','opened',
                'description','contact','realtime']

    def get_updated_at(self, obj):
        local_time = timezone.localtime(obj.updated_at)
        return local_time.strftime("%#m월 %#d일 %#H시 %#M분")
    
