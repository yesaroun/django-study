from django.db import models


class Lecture(models.Model):
    teacher = models.CharField(max_length=20)
    subject = models.CharField(max_length=20)
    lecturetime = models.DateTimeField()
    book = models.CharField(max_length=20)
