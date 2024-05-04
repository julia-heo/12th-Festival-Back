from django.shortcuts import get_object_or_404
from django.db.models import Q
import math
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .models import *
from .serializers import *
from .permissions import IsAuthorOrReadOnly
from .pagination import PaginationHandlerMixin


class CommentView(views.APIView):
    serializer_class = CommentPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, pk):
        booth = get_object_or_404(Booth, pk=pk)
        request.data['user']=request.user.id
        request.data['booth']=booth.id
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': '댓글 작성 성공', 'data': serializer.data}, status=HTTP_200_OK)
        else:
            return Response({'message': '댓글 작성 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)
        
    def get(self, request, pk):
        booth = get_object_or_404(Booth, pk=pk)
        comments = Comment.objects.filter(booth=pk)
        serializers = CommentSerializer(comments,many=True,context={'user': request.user.id})
        return Response({'message': '부스 댓글 조회 성공', 'data': serializers.data}, status=HTTP_200_OK)


class CommentDetailView(views.APIView): 
    permission_classes = [IsAuthorOrReadOnly]

    def get_object(self, pk):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(self.request, comment)
        return comment

    def delete(self, request,comment_pk):
        comment = self.get_object(pk=comment_pk)
        comment.delete()
        
        return Response({'message': '댓글 삭제 성공'}, status=HTTP_204_NO_CONTENT)
    
    def patch(self, request,comment_pk):
        comment = self.get_object(pk=comment_pk)
        serializer = CommentPostSerializer(comment, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': '댓글 수정 성공', 'data': serializer.data},status=HTTP_200_OK)
        else:
            return Response({'message': '댓글 수정 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)

class ChangeLikeView(views.APIView):
    serializer_class = BoothDetailSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        user = request.user
        booth = get_object_or_404(Booth, pk=pk)
        
        if booth.like.filter(id=user.id).exists():  
            booth.like.remove(user)
            is_liked = False
        else:  
            booth.like.add(user)
            is_liked = True

        booth.save()

        return Response({'message': '부스 스크랩 여부 변경 성공', 'data': {"booth":booth.id,"is_liked":is_liked}}, status=HTTP_200_OK)

class ChangeMenuLikeView(views.APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        user = request.user
        menu = get_object_or_404(Menu, pk=pk)
        
        if menu.like.filter(id=user.id).exists():  
            menu.like.remove(user)
            is_liked = False
        else:  
            menu.like.add(user)
            is_liked = True
            
        menu.save()

        return Response({'message': '메뉴 스크랩 여부 변경 성공', 'data': {"menu":menu.id,"is_liked":is_liked}}, status=HTTP_200_OK)


class BoothPagination(PageNumberPagination):
    page_size = 10

class SearchView(views.APIView,PaginationHandlerMixin):
    serializer_class = BoothListSerializer
    pagination_class = BoothPagination

    def get(self, request):
        page = request.GET.get('page', 1)
        user = request.user
        keyword= request.GET.get('keyword')
        search_type = request.GET.get('type')

        # 부스 정렬 기준 추가
        booths = (Booth.objects.filter(name__icontains=keyword) | Booth.objects.filter(menus__menu__contains=keyword)).distinct()

        if search_type == '부스':
            booths = booths.filter(performance=False)
        elif search_type == '공연':
            booths = booths.filter(performance=True)

        if user.is_authenticated:
            for booth in booths:
                if booth.like.filter(pk=user.id).exists():
                    booth.is_liked = True
        total = len(booths)
        total_page = math.ceil(total/10)
        serializer = self.serializer_class(booths, many=True)

        return Response({'message':'검색 성공', "page": page, 'total': total, 'total_page': total_page,"view": len(booths), 'data': serializer.data}, status=HTTP_200_OK)
    
    
class BoothDetailView(views.APIView):
    serializer_class = BoothDetailSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_object(self, pk):
        booth = get_object_or_404(Booth, pk=pk)
        self.check_object_permissions(self.request, booth)
        return booth

    def get(self, request, pk):
        user = request.user
        booth = self.get_object(pk=pk)

        if booth.like.filter(pk=user.id).exists():
            booth.is_liked=True

        serializer = self.serializer_class(booth,context={'user': request.user.id})

        return Response({'message': '부스 상세 조회 성공', 'data': serializer.data}, status=HTTP_200_OK)
    
class BoothListView(views.APIView):
    serializer_class = BoothListSerializer
    pagination_class = BoothPagination

    def get(self, request):
        day = request.GET.get('day', None)
        college = request.GET.get('college', None)
        type = request.GET.get('type')
        page = request.GET.get('page', 1)

        # 부스 정렬 기준 추가
        booths = Booth.objects.all()
        if type:
            if type == "공연":
                booths = booths.filter(performance=True)
            else:
                booths = booths.filter(performance=False)
        if day:
            booths = booths.filter(days__date=day)
        if college:
            if college is not None:
                booths = booths.filter(college=college)
        total = len(booths)
        total_page = math.ceil(total/10)
        if request.user.is_authenticated:
            for booth in booths:
                booth.is_liked = booth.like.filter(id=request.user.id).exists()
        serializers = self.serializer_class(booths, many=True)



        return Response({'message': "부스 목록 조회 성공","page":page, 'total': total, 
                        'total_page': total_page,"view": len(booths),'data': serializers.data}, status=HTTP_200_OK)
    

class HomeView(views.APIView):
    def get(self,request): 
        if not request.user.is_authenticated:
            return Response({'message':"로그인이 필요합니다."}, status=HTTP_401_UNAUTHORIZED)
        user = request.user
        nickname = request.user.nickname
        if user.is_booth == True:

            data = {
                "is_booth": True,
                "my_booth": Booth.objects.get(user=user).id,
                "is_tf":False,
                "nickname":nickname
            }
            return Response({'message':"부스 관리자 홈화면 조회 성공",'data':data}, status=HTTP_200_OK)
    
        if user.is_tf == True:

            data = {
                "is_booth": False,
                "my_booth": None,
                "is_tf":True,
                "nickname":nickname
            }
            return Response({'message':"tf 홈화면 조회 성공",'data':data}, status=HTTP_200_OK)
        
        # 부스 정렬 기준 추가
        booths = Booth.objects.filter(like=user.id,performance=False)[:4]
        for booth in booths:
            booth.is_liked=True
        boothList = BoothListSerializer(booths,many=True)

        menus = Menu.objects.filter(like=user.id)[:4]
        for menu in menus:
            menu.is_liked=True
        menuList = MenuListSerializer(menus,many=True)

        performs = Booth.objects.filter(like=user.id,performance=True)[:4]
        for perform in performs:
            perform.is_liked=True
        performList = BoothListSerializer(performs,many=True)

        total = len(booths) + len(menus) + len(performs)
        if(total == 0): scrap = False
        else: scrap = True

        data={
            "is_booth":False,
            "my_booth":None,
            "is_tf":False,
            "nickname":nickname,
            "scrap":scrap,
            "boothList":boothList.data,
            "menuList":menuList.data,
            "performList":performList.data
        }
        return Response({'message': "홈화면 조회 성공",'data': data}, status=HTTP_200_OK)
