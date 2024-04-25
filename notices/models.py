from django.db import models
from accounts.models import User
from booths.models import TimeStamp


class Notice(TimeStamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
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