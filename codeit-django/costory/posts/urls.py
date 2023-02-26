from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("posts/", views.PostListView.as_view(), name="post-list"),
    # path("posts/new", views.post_create, name="post-create"),
    path("posts/new", views.PostCreateView.as_view(), name="post-create"),
    path("posts/<int:post_id>/", views.post_detail, name="post-detail"),
    path("posts/<int:post_id>/edit", views.post_update, name="post-update"),
    path("posts/<int:post_id>/delete", views.post_delete, name="post-delete"),
]
