from django.urls import path
from .views import *

app_name = 'notices'

urlpatterns = [
    path('', NoticeListView.as_view()),
    path('<int:pk>/', NoticeDetailView.as_view()),
    path('event/', EventListView.as_view()),
    path('event/<int:pk>/', EventDetailView.as_view()),

]