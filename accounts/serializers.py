from rest_framework import serializers
from .models import *
from booths.models import Booth, Menu
from rest_framework_simplejwt.tokens import RefreshToken


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id', 'username', 'password', 'nickname', 'is_booth','is_tf']

    def create(self, validated_data):  
        user = User.objects.create(
            username=validated_data['username'],
            nickname=validated_data['nickname'],
            is_booth=False,
            is_tf=False
        )
        user.set_password(validated_data['password'])
        user.save()

        token = RefreshToken.for_user(user)
        refresh = str(token)
        access = str(token.access_token)
        
        return user, access
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if not user.check_password(password):
                raise serializers.ValidationError('잘못된 비밀번호입니다.')
            else:
                token = RefreshToken.for_user(user)
                refresh = str(token)
                access = str(token.access_token)

                data = {
                    'id': user.id,
                    'nickname': user.nickname ,
                    'access_token': access
                }

                return data
        else:
            raise serializers.ValidationError('존재하지 않는 사용자입니다.')


class ProfileSerializer(serializers.ModelSerializer):
    booth_id = serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=['id', 'nickname', 'is_booth','is_tf','booth_id']
    
    def get_booth_id(self, obj):
        if(obj.is_booth==True):
            return Booth.objects.get(user=obj).id
        else:
            return None


class LikeBoothSerializer(serializers.ModelSerializer):
    is_liked = serializers.BooleanField(default=False)
    info = serializers.SerializerMethodField()
    class Meta:
        model=Booth
        fields=['id', 'name', 'info','thumnail','opened','is_liked']
    
    def get_info(self, obj):
        return obj.college+" "+obj.number
    

class LikeMenuSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    is_liked = serializers.BooleanField(default=False)
    booth_id = serializers.SerializerMethodField()
    info = serializers.SerializerMethodField()
    thumnail = serializers.SerializerMethodField()
    opened = serializers.SerializerMethodField()
    class Meta:
        model=Menu
        fields=['id', 'name',"booth_id", 'info','thumnail','opened','is_liked']
    
    def get_name(self,obj):
        return obj.menu
    def get_booth_id(self,obj):
        return obj.booth.id
    def get_info(self, obj):
        return str(obj.price)+"원"
    def get_thumnail(self, obj):
        return obj.img
    def get_opened(self, obj):
        return not obj.is_soldout