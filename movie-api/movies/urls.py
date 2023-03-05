from django.urls import path
from .views import movie_list, actor_list, movie_detail, actor_detail


urlpatterns = [
    path("movies", movie_list),
    path("movies/<int:pk>", movie_detail),
    path("actors", actor_list),
    path("actors/<int:pk>", actor_detail),
]
