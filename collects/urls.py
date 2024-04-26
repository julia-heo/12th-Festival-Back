from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'collects'

urlpatterns = [
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('detail/', detail_view, name="detail"),
    path('update/<int:booth_id>', update_view, name="update"),
    path('password_change/',password_change_view,name="password_change"),
    path('update_menu/<int:menu_id>',update_menu_view,name="update_menu"),
    path('delete_menu/<int:menu_id>',delete_menu_view,name="delete_menu"),
    path('create_menu/<int:booth_id>',create_menu_view,name="create_menu")
]