from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsAuthorOrReadOnly
from .storages import FileUpload, s3_client
# Create your views here.

class MenuView(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MenuSerializer
    
    def get(self, request, pk):
        booth = get_object_or_404(Booth, pk=pk)
        menus = Menu.objects.filter(booth=booth)
        serializer = self.serializer_class(menus, many=True)    
        return Response({'message': '메뉴 목록 조회 성공', 'data': serializer.data}, status=HTTP_200_OK)

    def post(self, request, pk):
        data = request.data.copy() # request.data 자체 불변성 --> copy해서 편집
        data['booth'] = pk
        # serializer = MenuSerializer(data=data)

        if 'img' in data:
            if data['img'] == "":
                file_url = "https://festivalewha.s3.ap-northeast-2.amazonaws.com/menu_defalt.png"
                data.pop('img')

            else:
                file = request.FILES.get('img')
                data.pop('img')
                folder = f"{pk}_images"  
                file_url = FileUpload(s3_client).upload(file, folder)

                
            serializer = MenuSerializer(data=data)
            if serializer.is_valid():

                seri = serializer.save()   
                seri.img = file_url
                seri.save() 

                return Response({'message': '메뉴 등록 성공, 메뉴 사진 등록', 'data': serializer.data}, status=HTTP_201_CREATED)
            return Response({'message': '메뉴 등록 실패, 메뉴 사진 등록', 'error': serializer.errors}, status=HTTP_400_BAD_REQUEST)
    
        else:
            data['booth'] = pk
            # if 'img' not in data :
            data['img'] = "https://festivalewha.s3.ap-northeast-2.amazonaws.com/menu_defalt.png"
            serializer = MenuSerializer(data=data)
            if serializer.is_valid():
                seri = serializer.save()
                return Response({'message':'메뉴 등록 성공, 기본 이미지','data':serializer.data}, status=HTTP_201_CREATED)


class MenuDetailView(views.APIView):
    serializer_class = MenuSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_object(self, pk, menu_pk):
        booth = get_object_or_404(Booth, pk=pk)
        menu = get_object_or_404(Menu, pk=menu_pk, booth=booth)
        return menu
    
    def get(self, request, pk, menu_pk):
        menu = self.get_object(pk, menu_pk)
        serializer = self.serializer_class(menu)
        return Response({'message': '메뉴 상세 조회 성공', 'data': serializer.data})

    def delete(self, request, pk, menu_pk):
        menu = self.get_object(pk, menu_pk)
        menu.delete()
        return Response({'message': '메뉴 삭제 성공'}, status=HTTP_204_NO_CONTENT)

    def patch(self, request, pk, menu_pk):
        menu = get_object_or_404(Menu, pk=menu_pk, booth=pk) 
        serializer = MenuSerializer(instance=menu, data=request.data, partial=True)

        if 'img' in request.data:
            file = request.FILES['img']
            folder = f"{pk}_images"  
            file_url = FileUpload(s3_client).upload(file, folder)
            request.data['img'] = file_url

        if serializer.is_valid():
            serializer.save()
            return Response({'message': '메뉴 수정 성공', 'data': serializer.data}, status=HTTP_200_OK)
        return Response({'message': '메뉴 수정 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)

class ChangeLikeMenu(views.APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk, menu_pk):
        user = request.user
        menu = get_object_or_404(Menu, pk=menu_pk, booth=pk)

        if menu.like.filter(id=user.id).exists():  
            menu.like.remove(user)
            is_liked = False
        else:  
            menu.like.add(user)
            is_liked = True

        menu.is_liked = is_liked
        menu.save()

        serializer = MenuSerializer(menu, context={'request': request})

        return Response({'message': '메뉴 좋아요 여부 변경 성공', 'data': serializer.data}, status=HTTP_200_OK)
