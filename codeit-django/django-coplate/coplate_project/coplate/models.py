from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(
        max_length=15,
        unique=True,
        null=True,
    )

    def __str__(self) -> str:
        return self.email
