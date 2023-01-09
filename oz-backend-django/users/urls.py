from django.urls import path
from . import views

urlpatterns = [
    path("myinfo", views.MyInfo.as_view())
]