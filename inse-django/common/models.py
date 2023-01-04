from django.db import models


class CommonModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    # 다른 디비랑 같이 보이는게 싫으니까 Meta 클래스를 사용한다
    class Meta:
        abstract = True
        # 다른 모델의 추상화로 사용하겠다는 것이다.