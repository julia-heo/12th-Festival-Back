from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
        path('signup/',SignUpView.as_view()),
        path('login/',LoginView.as_view()),
        path('duplicate/',DuplicateUsernameView.as_view()),
        path('kakao/', KakaoLoginView.as_view()),
        path('kakao/callback/',KakaoCallbackView.as_view()),
        path('kakao/nickname', KakaoSignupView.as_view()),
        path('', ProfileView.as_view()),
        path('likes/',LikesView.as_view())
]