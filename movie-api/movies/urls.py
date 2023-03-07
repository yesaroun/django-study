from django.urls import path

# from .views import movie_list, actor_list, movie_detail, actor_detail, review_list
from .views import actor_list, actor_detail
from .views import MovieList, MovieDetail, ReviewList

urlpatterns = [
    # path("movies", movie_list),
    # path("movies/<int:pk>", movie_detail),
    # path("movies/<int:pk>/reviews", review_list),
    path("actors", actor_list),
    path("actors/<int:pk>", actor_detail),
    path("movies", MovieList.as_view()),
    path("movies/<int:pk>", MovieDetail.as_view()),
    path("movies/<int:pk>/reviews", ReviewList.as_view()),
]
