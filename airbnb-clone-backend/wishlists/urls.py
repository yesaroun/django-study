from django.urls import path
from .views import WishLists


urlpatterns = [
    path("", WishLists.as_view()),
]
