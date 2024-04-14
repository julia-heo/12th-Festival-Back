# import imp
import importlib.util
from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ['id', 'username', 'nickname', 'is_booth', 'created_at', 'updated_at']