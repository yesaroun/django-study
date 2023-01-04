from django.db import models
from users.models import User
from common.models import CommonModel


class Feed(CommonModel):
# class Feed(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    img = models.ImageField(blank=True, null=True)
    like = models.PositiveIntegerField()
    content = models.TextField(max_length=200)
    # review_id

## Feed
## - User
## - img
## - created_at
## - updated_at
## - like
## - content
## - Review (댓글)