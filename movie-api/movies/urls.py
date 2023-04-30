from django.contrib import admin
from django.urls import path

# from .views import movie_list, actor_list, movie_detail, actor_detail, review_list
from .views import actor_list, actor_detail
from .views import MovieList, MovieDetail, ReviewList
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="movie api",
        default_version="1.0.0",
        description="movie API 문서",
    ),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("movies", movie_list),
    # path("movies/<int:pk>", movie_detail),
    # path("movies/<int:pk>/reviews", review_list),
    path(
        "swagger/schema/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="swagger-schema",
    ),
    path("actors", actor_list),
    path("actors/<int:pk>", actor_detail),
    path("movies", MovieList.as_view()),
    path("movies/<int:pk>", MovieDetail.as_view()),
    path("movies/<int:pk>/reviews", ReviewList.as_view()),
]
