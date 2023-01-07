from django.db import models

class User(models.Model):
    name = models.CharField(max_length=20)  # Model을 상속받는다.
    description = models.TextField()        # 긴 텍스트 문장
    age = models.PositiveIntegerField()     # 양의 정수형
    sex = models.CharField(max_length=10)
    is_business = models.BooleanField(default=False)

    def __str__(self):
        return self.name
