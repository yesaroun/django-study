# from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # nickname = models.CharField(max_length=30)
    # phone = models.PositiveIntegerField()       # 양의 정수형 숫자
    # is_business = models.BooleanField(default=False)    # boolean은 default값이 있어야 한다.
    # gender = models.CharField(max_length=10)
    # profileIntroduce = models.TextField(max_length=200)
    # sns = models.CharField(max_length=10, default="")
    pass