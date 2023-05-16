from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(
        max_length=15,
        unique=True,
        null=True
    )
    kakao_id = models.CharField(
        max_length=20,
        null=True,
    )
    address = models.CharField(
        max_length=40,
        null=True,
    )
    
    def __str__(self) -> str:
        return self.email