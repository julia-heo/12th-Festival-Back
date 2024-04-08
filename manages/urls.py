from django.urls import path
from .views import *

app_name = 'manage'

urlpatterns = [
    path('<int:pk>/menus/', MenuListView.as_view()),
    path('<int:pk>/menus/<int:menu_pk>/', MenuDetailView.as_view()),
]