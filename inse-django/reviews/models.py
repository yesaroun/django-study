from django.db import models

class Review(models.Model):
    # user =
    content = models.CharField(max_length=120)
    like = models.PositiveIntegerField()
    reply = models.BooleanField(default=False)