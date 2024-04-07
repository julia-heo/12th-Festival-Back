from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import views
from rest_framework.status import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import *
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from .pagination import PaginationHandlerMixin
from .permissions import IsTFOrReadOnly

class TFPagination(PageNumberPagination):
    page_size = 5

class NoticeListView(views.APIView):
    serializer_class = NoticeSerializer
    pagination_class = TFPagination
    permission_classes = [IsTFOrReadOnly]

    def get(self, request):
        notices = Notice.objects.all().order_by('-created_at')
        paginator = self.pagination_class()
        notices_page = paginator.paginate_queryset(notices, request)
        serializer = self.serializer_class(notices_page, many=True)
        page_number = request.GET.get('page', 1)
        
        if notices.exists(): 
            total_items = Notice.objects.count()
            total_pages = paginator.page.paginator.num_pages
            view_count = len(serializer.data)

            return Response({'message': 'TF 공지 조회 성공','page': page_number,'total': total_items,'total_page': total_pages,'view': view_count,'data': serializer.data}, status=HTTP_200_OK)
        else: 
            return Response({'message': 'TF 공지 없음','page': page_number,'total': Notice.objects.count(),'total_page': paginator.page.paginator.num_pages,'view': 0,'data': serializer.data}, status=HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response({'message': 'TF 공지 작성 성공', 'data': serializer.data}, status=HTTP_200_OK)
        else:
            return Response({'message': 'TF 공지 작성 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)


class NoticeDetailView(views.APIView):
    serializer_class = NoticeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsTFOrReadOnly]


    def get_object(self, pk):
        notice = get_object_or_404(Notice, pk=pk)
        self.check_object_permissions(self.request, notice)

        return notice

    def get(self, request, pk):
        notice = self.get_object(pk=pk)
        serializer = self.serializer_class(notice)

        return Response({'message': 'TF 공지 상세 조회 성공', 'data': serializer.data})

    def put(self, request, pk):
        notice = self.get_object(pk=pk)
        serializer = self.serializer_class(data=request.data, instance=notice)

        if serializer.is_valid():
            serializer.save()
            return Response({'message' : 'TF 공지 수정 성공', 'data': serializer.data}, status = HTTP_200_OK)
        return Response({'message': 'TF 공지 수정 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        notice = self.get_object(pk=pk)
        notice.delete()

        return Response({'message': 'TF 공지 삭제 성공'}, status=HTTP_204_NO_CONTENT)
    