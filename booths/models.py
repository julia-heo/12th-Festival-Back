from django.db import models
from accounts.models import User

class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    
class Booth(TimeStamp):
    COLLEGE_CHOICES = (
        ('교육관', '교육관'),
        ('대강당', '대강당'),
        ('신세계관', '신세계관'),
        ('생활관', '생활관'),
        ('정문', '정문'),
        ('포스코관', '포스코관'),
        ('학문관', '학문관'),
        ('휴웃길', '휴웃길'),
        ('학관', '학관'),
        ('잔디광장', '잔디광장')
        # 공연 위치정보 추가
    )
    CATEGORY_CHOICES = (
        ('음식', '음식'),
        ('굿즈', '굿즈'),
        ('체험', '체험'),
        ('기타', '기타'),
        # 공연 카테고리 추가
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    college = models.CharField(choices=COLLEGE_CHOICES, max_length=20)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=5)
    name = models.TextField()
    number = models.CharField(max_length=10, blank=True)
    thumnail = models.TextField(null=True, blank=True)
    opened = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    like = models.ManyToManyField(User, related_name='booths', blank=True)
    contact = models.TextField(blank=True)              # 운영진 연락처 
    realtime = models.TextField(blank=True)             # 실시간 공지사항
    performance = models.BooleanField(default=False)    # 공연 여부 (부스False 공연True)
    
    def __str__(self):
        return self.name
    
class Day(models.Model):
    DAY_CHOICES = (
        ('수요일', '수요일'),
        ('목요일', '목요일'),
        ('금요일', '금요일'),
    )
    DATE_CHOICES = (
        (8, 8),
        (9, 9),
        (10, 10),
    )
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='days')
    day = models.CharField(choices=DAY_CHOICES, max_length=5)
    date = models.IntegerField(choices=DATE_CHOICES)
    start_time=models.CharField(max_length=5,null=False,blank=False)
    end_time=models.CharField(max_length=5,null=False,blank=False)

    def __str__(self):
        return f'{self.id}'
    
class Menu(TimeStamp):
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='menus')
    menu = models.TextField()
    price = models.PositiveIntegerField()
    is_soldout = models.BooleanField(default=False)
    like = models.ManyToManyField(User, related_name='menus', blank=True)
    img = models.TextField(null=True, blank=True)
    vegan=models.CharField(null=True, max_length=5)

    def __str__(self):
        return f'{self.menu}'

class Comment(TimeStamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()

class Event(TimeStamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    place=models.TextField()        #장소 필터링 + 넘버 없음
    summary=models.TextField()      #리스트 목록에 보이는 한마디
    thumnail = models.TextField(null=True, blank=True)
    opened = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    contact = models.TextField(blank=True)              
    realtime = models.TextField(blank=True)             
    
    
    def __str__(self):
        return self.name
    

class EventComment(TimeStamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_comments')
    event = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='event_comments')
    content = models.TextField()