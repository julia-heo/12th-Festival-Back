from rest_framework import serializers

from booths.models import *
from accounts.models import User


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id','booth', 'menu', 'price', 'is_soldout','like','img', 'vegan']

class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = ['id', 'day', 'date', 'start_time', 'end_time']

class BoothDetailSerializer(serializers.ModelSerializer):
    days = DaySerializer(many=True, read_only=True)

    class Meta:
        model = Booth
        fields = ['id', 'user', 'college', 'name', 'days', 'number', 'thumnail', 'opened', 'description', 'contact', 'realtime', 'performance']
