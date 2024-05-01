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
    path('create_menu/<int:booth_id>',create_menu_view,name="create_menu"),
    path('event/list/',event_list_view,name="event_list"),
    path('event/detail/<int:event_id>',event_detail_view,name="event_detail"),
    path('event/addpage/',event_add_page_view,name="event_add_page"),
    path('event/add/',event_add_view,name="event_add"),
    path('event/update/<int:event_id>',event_update_view,name="event_update"),
    path('event/delete/<int:event_id>',event_delete_view,name="event_delete"),
]