from django.db import models
from accounts.models import User
from booths.models import TimeStamp


class Notice(TimeStamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()