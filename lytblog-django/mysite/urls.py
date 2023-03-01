from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("bookmark/", include("bookmark.urls")),
    path("blog/", include("blog.urls")),
]
