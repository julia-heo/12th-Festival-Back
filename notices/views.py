from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import views
from rest_framework.status import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import *
from booths.models import * 
from manages.storages import FileUpload, s3_client
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from .pagination import PaginationHandlerMixin
from .permissions import IsTFOrReadOnly
#from PIL import Image
from django.core.files.base import ContentFile
import io
from django.core.files import File
import os
import tempfile
import boto3
from PIL import Image as pil
import os

def rescale(image, width):
    # 이미지 크기 조절
    img = pil.open(image)
    src_width, src_height = img.size
    src_ratio = float(src_height) / float(src_width)
    dst_height = round(src_ratio * width)

    size=width, dst_height
    img.thumbnail(size, pil.LANCZOS)
    img = img.convert("RGB")
    filename=str(image)
    resultPath="./collects/tempfiles"
    temp_file_path=os.path.join(resultPath, filename)
    img.save(temp_file_path)

    size_kb = os.path.getsize(temp_file_path) / 1024
    print(size_kb)
    while os.path.getsize(temp_file_path) / 1024 > 500:
        width/=2
        dst_height/=2
        size=width, dst_height
        img.thumbnail(size, pil.LANCZOS)
        img = img.convert("RGB")
        img.save(temp_file_path)
        size_kb = os.path.getsize(temp_file_path) / 1024
        print(size_kb)
    return temp_file_path,filename

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

    def put(self, request, pk, format=None):
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


class EventListView(views.APIView):
    serializer_class = EventListSerializer
    permission_classes = [IsTFOrReadOnly]
    
    def get(self, request):
        event_type = request.query_params.get('type')
        if event_type not in ['1', '2', '3']:
            return Response({'message': '올바르지 않은 이벤트 타입입니다.'}, status=400)
        if event_type == '1':
            events = Event.objects.filter(type='기획부스')
            message = "기획부스 이벤트 목록입니다."
        elif event_type == '2':
            events = Event.objects.filter(type='권리팀부스')
            message = "권리팀부스 이벤트 목록입니다."
        elif event_type == '3':
            events = Event.objects.filter(type='대외협력팀부스')
            message = "대외협력팀부스 이벤트 목록입니다."
        serializer = EventListSerializer(events, many=True)
    
        response_data = {
            'message': message,
            'events': serializer.data
        }
        return Response(response_data)

class EventDetailView(views.APIView):
    serializer_class = EventDetailSerializer
    permission_classes = [IsTFOrReadOnly]
    def get_object(self, pk):
        event = get_object_or_404(Event, pk=pk)
        self.check_object_permissions(self.request, event)

        return event

    def get(self, request, pk):
        event = self.get_object(pk=pk)
        serializer = self.serializer_class(event)
        return Response({'message': 'TF 부스 상세 조회 성공', 'data': serializer.data})
    
    def patch(self, request, pk, format=None):
        event = self.get_object(pk)
        request_data = request.data.copy() 
        

        if 'thumnail' in request_data:
            file = request.FILES['thumnail']
            folder = f"{pk}_images"   
            temp_file_path,name = rescale(file,700)
            file_extension = name.split('.')[-1]

            file_url = FileUpload(s3_client).upload(open(temp_file_path, 'rb'), folder, "thumnail"+str(pk)+"."+file_extension)
            request_data['thumnail'] = file_url
            os.remove(temp_file_path)
        else:
            request_data['thumnail'] = ""

        serializer = EventDetailSerializer(instance=event, data=request_data, partial=True)
            #img = Image.open(thumnail_file)
            #temp = io.BytesIO()
            #img.save(temp, format='JPEG', quality=40)
            #temp.seek(0)
            #compressed_image_url = FileUpload(s3_client).upload(temp, folder)
            #request.data['thumnail'] = compressed_image_url

        if serializer.is_valid():
            serializer.save()

            request_days = request.data.get('days', [])
            existing_days = event.days.all()

            for request_day in request_days:
                date = request_day.get('date')
                existing_day = existing_days.filter(date=date).first()

                if existing_day:
                    existing_day.start_time = request_day.get('start_time')
                    existing_day.end_time = request_day.get('end_time')
                    existing_day.save()
                else:
                    day_of_week = self.get_day_from_date(date) 
                    event.days.create(
                        date=date,
                        day=day_of_week,
                        start_time=request_day.get('start_time'),
                        end_time=request_day.get('end_time')
                    )

            return Response({'message': 'TF 부스 수정 성공', 'data': serializer.data}, status=HTTP_200_OK)
        else:
            return Response({'message': 'TF 부스 수정 실패', 'errors': serializer.errors}, status=HTTP_400_BAD_REQUEST)

    def get_day_from_date(self, date):
        date_day_mapping = {
            8: '수요일',
            9: '목요일',
            10: '금요일'
        }
        return date_day_mapping.get(date)

