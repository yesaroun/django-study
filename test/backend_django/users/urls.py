from django.urls import path
from .views import Users

urlpatterns = [
    path("", Users.as_view())
]
