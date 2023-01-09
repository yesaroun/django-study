from django.contrib import admin
from .models import Lecture


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ("teacher", "subject", "lecturetime", "book")
