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
from .storages import FileUpload, s3_client


class CommentView(views.APIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, pk):
        booth = get_object_or_404(Booth, pk=pk)
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, booth=booth)
            return Response({'message': '댓글 작성 성공', 'data': serializer.data}, status=HTTP_200_OK)
        else:
            return Response({'message': '댓글 작성 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)
    

class CommentDetailView(views.APIView): 
    permission_classes = [IsAuthorOrReadOnly]

    def get_object(self, pk):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(self.request, comment)
        return comment

    def delete(self, request, pk, comment_pk):
        comment = self.get_object(pk=comment_pk)
        comment.delete()
        
        return Response({'message': '댓글 삭제 성공'}, status=HTTP_204_NO_CONTENT)
    
    def patch(self, request,pk,comment_pk):
        comment = self.get_object(pk=comment_pk)
        serializer = self.serializer_class(comment, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': '댓글 수정 성공', 'data': serializer.data},status=HTTP_204_NO_CONTENT)
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

        booth.is_liked = is_liked
        booth.save()

        serializer = self.serializer_class(booth, context={'request': request})

        return Response({'message': '부스 좋아요 여부 변경 성공', 'data': serializer.data}, status=HTTP_200_OK)

class BoothPagination(PageNumberPagination):
    page_size = 10

class SearchView(views.APIView,PaginationHandlerMixin):
    serializer_class = BoothListSerializer
    pagination_class = BoothPagination

    def get(self, request):
        user = request.user
        keyword= request.GET.get('keyword')
        search_type = request.GET.get('type')

        booths = (Booth.objects.filter(name__icontains=keyword) | Booth.objects.filter(menus__menu__contains=keyword)).distinct()

        if search_type == '부스':
            booths = Booth.objects.filter(
                Q(name__icontains=keyword) |
                Q(menus__menu__icontains=keyword)
            ).distinct()
        elif search_type == '공연':
            booths = Booth.objects.filter(
                performances__name__icontains=keyword
            ).distinct()
        else:
            booths = Booth.objects.all()

        if user.is_authenticated:
            for booth in booths:
                if booth.like.filter(pk=user.id).exists():
                    booth.is_liked = True

        serializer = self.serializer_class(booths, many=True)


        return Response({'message':'부스 검색 성공', 'data': serializer.data}, status=HTTP_200_OK)
    
    
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

        serializer = self.serializer_class(booth)

        return Response({'message': '부스 상세 조회 성공', 'data': serializer.data}, status=HTTP_200_OK)
    
class BoothListView(views.APIView):
    serializer_class = BoothListSerializer
    pagination_class = BoothPagination

    def get(self, request):
        day = request.GET.get('day', None)
        college = request.GET.get('college', None)
        type = request.GET.get('type')
        page = request.GET.get('page', 1)

        booths = Booth.objects.all()
        if day:
            booths = booths.filter(day=day)
        if college:
            booths = booths.filter(college=college)
        if type:
            booths = booths.filter(type=type)
        total = len(booths)
        total_page = math.ceil(total/10)
        serializer = self.serializer_class(booths, many=True)



        return Response({'message': "부스 목록 조회 성공","page":page, 'total': total, 
                        'total_page': total_page,"view": len(booths),'data': serializers.data}, status=HTTP_200_OK)
    

class HomeView(views.APIView):
    def get(self,request):
        user = request.user
        nickname = request.user.nickname
        type = request.GET.get('type')
        
        if(type=="부스"):
            booths = Booth.objects.filter(like=user.id,performance=False)[:4]
            for booth in booths:
                booth.is_liked=True
            total = len(booths)
            if (total==0):
                return Response({'message': "스크랩한 부스가 없습니다", 'data': None}, status=HTTP_200_OK)
            serializers = BoothListSerializer(booths,many=True)
            return Response({'message': "스크랩한 부스 목록 조회 성공",'data': serializers.data}, status=HTTP_200_OK)
        
        elif(type=="메뉴"):
            menus = Menu.objects.filter(like=user.id)[:4]
            for menu in menus:
                menu.is_liked=True
            total = len(menus)
            if (total==0):
                return Response({'message': "스크랩한 메뉴가 없습니다",'data': None}, status=HTTP_200_OK)
            menus = self.paginate_queryset(menus)
            serializers = MenuSerializer(menus,many=True)
            return Response({'message': "스크랩한 메뉴 목록 조회 성공",'data': serializers.data}, status=HTTP_200_OK)

        elif(type=="공연"):
            booths = Booth.objects.filter(like=user.id,performance=True)[:4]
            for booth in booths:
                booth.is_liked=True
            total = len(booths)
            if (total==0):
                return Response({'message': "스크랩한 공연이 없습니다",'data': None}, status=HTTP_200_OK)
            booths = self.paginate_queryset(booths)
            serializers = BoothListSerializer(booths,many=True)
            return Response({'message': "스크랩한 공연 목록 조회 성공",'data': serializers.data}, status=HTTP_200_OK)
        else:
            return Response({'message': "type을 입력해주세요"}, status=HTTP_400_BAD_REQUEST)
      
       