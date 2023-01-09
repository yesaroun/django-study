from django.db import models

# Create your models here.
# class User(models.Model): # Model을 상속받는다
# 	name = models.CharField(max_length=20) # 짧은 문장
# 	description = models.TextField() # 긴 텍스트 문장
# 	age = models.PositiveIntegerField() # 양의 정수형 숫자 
# 	sex = models.CharField(max_length=10)
# 	is_business = models.BooleanField(default=False)

# 	def __str__(self):
# 		return self.name

from django.contrib.auth.models import AbstractUser
from common.models import CommonModel

class User(AbstractUser):
	# pass

    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male") # value, show
        FEMALE = ("female", "Female") # value, show

    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
    name = models.CharField(max_length=150, default="")
    is_business = models.BooleanField(default=False)
    gender = models.CharField(max_length=20, choices=GenderChoices.choices, default="female")
    # multi_sns = models.

    # created = models.DateTimeField(auto_now_add=True) # 해당 object 생성 시간을 기준
    # updated = models.DateTimeField(auto_now=True) # 해당 object가 업데이트된 시간을 기준
       


class SNS(models.Model):
    email = models.CharField(max_length=150)
    token = models.CharField(max_length=150, null=True)