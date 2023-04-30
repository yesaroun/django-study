from django.db import models
from users.models import User
from common.models import CommonModel


class Feed(CommonModel):
# class Feed(models.Model):
    img = models.ImageField(blank=True, null=True)
    like = models.PositiveIntegerField()
    content = models.TextField(max_length=200)
    # review_id

    user_id = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True)
    # user_id = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.content

## Feed
## - User
## - imgs
## - created_at
## - updated_at
## - like
## - content
## - Review (댓글)