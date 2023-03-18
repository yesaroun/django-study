from django.contrib import admin
from django.urls import path, include
from pboard.views import base_views
from typing import List

urlpatterns: List[path] = [
    path("admin/", admin.site.urls),
    path("pboard/", include("pboard.urls")),
    path("common/", include("common.urls")),
    path("", base_views.index, name="index"),
]
