from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=30)
    opening_date = models.DateField()
    running_time = models.IntegerField()
    overview = models.TextField()


class Actor(models.Model):
    name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1)
    birth_date = models.DateField()
