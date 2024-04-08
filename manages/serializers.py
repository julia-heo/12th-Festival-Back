from rest_framework import serializers

from .models import Booth, Menu, Image, Comment, Notice, Time
from accounts.models import User


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id','booth', 'menu', 'price', 'is_soldout','like','img']
