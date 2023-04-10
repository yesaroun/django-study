from django.urls import path
from .views import WishLists, WishlistsDetail, WishlistToggle


urlpatterns = [
    path("", WishLists.as_view()),
    path("<int:pk>", WishlistsDetail.as_view()),
    path("<int:pk>/rooms/<int:room_pk>", WishlistToggle.as_view()),
]
