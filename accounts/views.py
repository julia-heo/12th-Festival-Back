from django.shortcuts import render, redirect
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
import festival
from .models import *
from .serializers import *
import requests
import math
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .pagination import PaginationHandlerMixin
from rest_framework.decorators import api_view


# # Create your views here.
KAKAO_CLIENT_ID = getattr(festival.settings.base, 'KAKAO_CLIENT_ID')
KAKAO_APP_ID = getattr(festival.settings.base, 'KAKAO_APP_ID')
KAKAO_CLIENT_SECRET_KEY = getattr(festival.settings.base, 'KAKAO_CLIENT_SECRET_KEY')
KAKAO_REDIRECT_URI = getattr(festival.settings.base, 'KAKAO_REDIRECT_URI')
KAKAO_USERNAME = getattr(festival.settings.base, 'KAKAO_USERNAME')
KAKAO_PASSWORD = getattr(festival.settings.base, 'KAKAO_PASSWORD')
KAKAO_LOGIN_URI = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_URI = "https://kauth.kakao.com/oauth/token"
KAKAO_PROFILE_URI = "https://kapi.kakao.com/v2/user/me"


class SignUpView(views.APIView):
    authentication_classes = ()
    def post(self,request, format=None):
        serializer = SignUpSerializer(data=request.data)
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
    def post(self, request):
        return Response({'message': "아이디 중복 확인 성공","data":{"duplicate":User.objects.filter(username=request.data['username']).exists()}}, status=HTTP_200_OK)

class KakaoLoginView(views.APIView):
    def get(self, request):
        uri = f"{KAKAO_LOGIN_URI}?client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_REDIRECT_URI}&response_type=code"
        
        res = redirect(uri)
        # res = requests.get(uri)
        print(res.get("access_tocken"))
        return res

class KakaoCallbackView(views.APIView):
    def get(self, request):         
        # access_token 발급 요청
        code = request.GET.get('code')
        if not code:
            return Response(status=HTTP_400_BAD_REQUEST)

        request_data = {
            'grant_type': 'authorization_code',
            'client_id': KAKAO_CLIENT_ID,
            'redirect_uri': KAKAO_REDIRECT_URI,
            'client_secret': KAKAO_CLIENT_SECRET_KEY,
            'code': code,
        }
        token_headers = {
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        token_res = requests.post(KAKAO_TOKEN_URI, data=request_data, headers=token_headers)

        token_json = token_res.json()
        access_token = token_json.get('access_token')

        if not access_token:
            return Response(status=HTTP_400_BAD_REQUEST)
        access_token = f"Bearer {access_token}" \

        # kakao 회원정보 요청
        auth_headers = {
            "Authorization": access_token,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        user_info_res = requests.post(KAKAO_PROFILE_URI, headers=auth_headers)
        user_info_json = user_info_res.json()
        social_id = str(user_info_json.get('id'))

        # 회원가입 및 로그인 처리 
        try:   
            user_in_db = User.objects.get(username=KAKAO_USERNAME+social_id) 
            # kakao계정 아이디가 이미 가입한거라면
            # 서비스에 rest-auth 로그인
            data={'username':KAKAO_USERNAME+social_id,'password':KAKAO_PASSWORD}
            serializer = KakaoLoginSerializer(data=data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                validated_data['exist'] = True
                return Response({'message': "카카오 로그인 성공", 'data': validated_data}, status=HTTP_200_OK)
            return Response({'message': "카카오 로그인 실패", 'error': serializer.errors}, status=HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:   
            return Response({'message':'카카오 회원가입 진행','data':{"exist":False,"username":social_id}}, status=HTTP_201_CREATED)

class KakaoSignupView(views.APIView):
    def post(self, request):  
        request_data=request.data
        request_data['username']=KAKAO_USERNAME+request.data['username']
        request_data['password']=KAKAO_PASSWORD
        serializer = SignUpSerializer(data=request_data)
        if serializer.is_valid():
            user, access = serializer.save()
            data={"id":user.id,"nickname":user.nickname,"access_token":access}
            return Response({'message':'닉네임 등록, 카카오 회원가입 완료','data':data}, status=HTTP_201_CREATED)
        return Response({'message':'카카오','error':serializer.errors},status=HTTP_400_BAD_REQUEST)
    
class ProfileView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):  
        user=request.user
        serializer = ProfileSerializer(user)
        return Response({'message':'프로필 조회 성공','data':serializer.data}, status=HTTP_201_CREATED)

class LikePagination(PageNumberPagination):
    page_size = 10

class LikesView(views.APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticated]
    pagination_class = LikePagination
    def get(self, request):  
        user=request.user
        type = request.GET.get('type')
        page = request.GET.get('page', '1')
        nickname=user.nickname
        # 부스 정렬 기준 추가
        if(type=="부스"):
            booths = Booth.objects.filter(like=user.id,performance=False)
            for booth in booths:
                booth.is_liked=True
            total = len(booths)
            if (total==0):
                return Response({'message': "스크랩한 부스가 없습니다","page":(int)(page), 'total': 0, 'total_page': 0,"view": 0,'data': None,'nickname':nickname}, status=HTTP_200_OK)
            total_page = math.ceil(total/10)
            booths = self.paginate_queryset(booths)
            serializers = LikeBoothSerializer(booths,many=True)
            return Response({'message': "스크랩한 부스 목록 조회 성공","page":(int)(page), 'total': total, 'total_page': total_page,"view": len(booths),'nickname':nickname, 'data': serializers.data}, status=HTTP_200_OK)

        elif(type=="메뉴"):
            menus = Menu.objects.filter(like=user.id)
            for menu in menus:
                menu.is_liked=True
            total = len(menus)
            if (total==0):
                return Response({'message': "스크랩한 메뉴가 없습니다","page":(int)(page), 'total': 0, 'total_page': 0,"view": 0,'data': None, 'nickname':nickname}, status=HTTP_200_OK)
            total_page = math.ceil(total/10)
            menus = self.paginate_queryset(menus)
            serializers = LikeMenuSerializer(menus,many=True)
            return Response({'message': "스크랩한 메뉴 목록 조회 성공","page":(int)(page), 'total': total, 'total_page': total_page,"view": len(menus),'nickname':nickname,'data': serializers.data}, status=HTTP_200_OK)

        elif(type=="공연"):
            booths = Booth.objects.filter(like=user.id,performance=True)
            for booth in booths:
                booth.is_liked=True
            total = len(booths)
            if (total==0):
                return Response({'message': "스크랩한 공연이 없습니다","page":(int)(page), 'total': 0, 'total_page': 0,"view": 0,'data': None, 'nickname':nickname}, status=HTTP_200_OK)
            total_page = math.ceil(total/10)
            booths = self.paginate_queryset(booths)
            serializers = LikeBoothSerializer(booths,many=True)
            return Response({'message': "스크랩한 공연 목록 조회 성공","page":(int)(page), 'total': total, 'total_page': total_page,"view": len(booths),'nickname':nickname,'data': serializers.data}, status=HTTP_200_OK)
        else:
            return Response({'message': "type을 입력해주세요"}, status=HTTP_400_BAD_REQUEST)
    
class HealthView(views.APIView):
    @api_view(['GET','POST'])
    def health(request):
        return Response(status=HTTP_200_OK)
