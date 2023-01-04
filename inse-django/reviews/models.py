from django.db import models
from common.models import CommonModel

class Review(CommonModel):
# class Review(models.Model):
    # user =
    content = models.CharField(max_length=120)
    like = models.PositiveIntegerField()
    reply = models.BooleanField(default=False)