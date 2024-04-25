from django.contrib import admin
from .models import *

@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
	list_display = ['id','day', 'booth','start_time','end_time']
	list_display_links = ['id','day']

@admin.register(Booth)
class BoothAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'user', 'created_at', 'updated_at','performance']
	list_display_links = ['id','name']

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
	list_display = ['id', 'menu', 'booth', 'price', 'is_soldout', 'created_at', 'updated_at']
	list_display_links = ['id', 'menu']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'booth', 'content', 'created_at', 'updated_at']

@admin.register(Event)
class EvnetAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'user', 'created_at', 'updated_at']
	list_display_links = ['id','name']

@admin.register(EventDay)
class EventDayAdmin(admin.ModelAdmin):
	list_display = ['id','day', 'event','start_time','end_time']
	list_display_links = ['id','day']
