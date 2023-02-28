from django.contrib import admin
from django.urls import path
from bookmark.views import BookmarkLV, BookmarkDV

urlpatterns = [
    path("admin/", admin.site.urls),
    # class-based views
    path("bookmark/", BookmarkLV.as_view(), name="index"),
    path("bookmakr/<int:pk>", BookmarkDV.as_view(), name="detail"),
]
