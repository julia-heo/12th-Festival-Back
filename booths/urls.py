from django.urls import path
from .views import *

app_name = 'booths'

urlpatterns = [
    path('home/', HomeView.as_view()),
    path('', BoothListView.as_view()),
    path('search/', SearchView.as_view()),
    path('<int:pk>/', BoothDetailView.as_view()),
    path('<int:pk>/likes/', ChangeLikeView.as_view()),
    path('<int:pk>/menu/', ChangeMenuLikeView.as_view()),
    path('<int:pk>/comments/', CommentView.as_view()),
    path('comments/<int:comment_pk>/', CommentDetailView.as_view()),
]