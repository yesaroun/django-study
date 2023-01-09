from django.db import models
from common.models import CommonModel
# Create your models here.
"""
Img
Content
Like
Reviews
"""
# class Feed(models.Model):
class Feed(CommonModel):
    # img = ""
    content = models.CharField(max_length=300)
    like = models.PositiveIntegerField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE) # user를 지우면 feed도 같이 지워진다.
    # user = models.ForeignKey("users.User", on_delete=models.SET_NULL) # user를 지우면 feed에서 user 데이터만 지워진다.

    def __str__(self):
        return self.content

class Tag(CommonModel):
    name = models.CharField(max_length=10)
    feeds = models.ManyToManyField(Feed)
    