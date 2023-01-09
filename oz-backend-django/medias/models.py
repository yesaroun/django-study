from django.db import models
from common.models import CommonModel

class Photo(CommonModel):
    file = models.ImageField() # ImageField를 사용하려면 pillow 설치 필요 > poetry add pillow
    description = models.CharField(max_length=140,)
    feed = models.ForeignKey(
        "feeds.Feed",
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return f"{self.file}"

class Video(CommonModel):

    file = models.FileField()
    feed = models.ForeignKey(
        "feeds.Feed",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.file}"
