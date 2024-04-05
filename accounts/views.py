from django.shortcuts import render
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
import festival
from .models import *
from .serializers import *

# # Create your views here.
KAKAO_CLIENT_ID=getattr(festival.settings.base, 'KAKAO_CLIENT_ID')
KAKAO_APP_ID=getattr(festival.settings.base, 'KAKAO_APP_ID')
KAKAO_CLIENT_SECRET_KEY=getattr(festival.settings.base, 'KAKAO_CLIENT_SECRET_KEY')
KAKAO_REDIRECT_URI=getattr(festival.settings.base, 'KAKAO_REDIRECT_URI')


class SignUpView(views.APIView):
    serializer_class = SignUpSerializer
    def post(self,request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user, access = serializer.save()
            returndata={"id":user.id,"nickname":user.nickname,"access_token":access}
            return Response({'message':'회원가입 성공','data':returndata}, status=HTTP_201_CREATED)
        return Response({'message':'회원가입 실패','error':serializer.errors},status=HTTP_400_BAD_REQUEST)
    
class LoginView(views.APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message': "로그인 성공", 'data': serializer.validated_data}, status=HTTP_200_OK)
        return Response({'message': "로그인 실패", 'error': serializer.errors}, status=HTTP_400_BAD_REQUEST)
    
class DuplicateUsernameView(views.APIView):
    def get(self, request):
        return Response({'message': "아이디 중복 확인 성공","data":{"duplicate":User.objects.filter(username=request.data['username']).exists()}}, status=HTTP_200_OK)

       