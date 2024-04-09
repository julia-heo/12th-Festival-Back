from django.urls import path
from .views import *

app_name = 'manages'

urlpatterns = [
    #path('<int:pk>/', BoothDetailView.as_view()),
    path('<int:pk>/menus/', MenuView.as_view()),
    path('<int:pk>/menus/<int:menu_pk>/', MenuDetailView.as_view()),
]