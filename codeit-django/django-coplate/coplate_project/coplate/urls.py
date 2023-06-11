from django.urls import path
from . import views


urlpatterns = [
    path(
        "",
        views.IndexView.as_view(),
        name="index",
    ),
    path(
        "reivews/<int:review_id>/",
        views.ReviewDetailView.as_view(),
        name="review-detail",
    ),
    path(
        "reviews/new/",
        views.ReviewCreateView.as_view(),
        name="review-create",
    ),
    path(
        "reviews/<int:review_id>/edit/",
        views.ReviewUpdateView.as_view(),
        name="review-update",
    ),
    path(
        "reviews/<int:review_id>/delete/",
        views.ReviewDeleteView.as_view(),
        name="review-delete",
    ),
    path("users/<int:user_id>/", views.ProfileView.as_view(), name="profile"),
    path(
        "urls/<int:user_id>/reviews",
        views.UserReviewListView.as_view(),
        name="user-review-list",
    ),
]
