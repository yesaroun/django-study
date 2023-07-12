from django.urls import path

from coplate.views import pure_views, drf_views

urlpatterns = [
    # review
    path("", pure_views.IndexView.as_view(), name="index"),
    path("reviews/", pure_views.ReviewListView.as_view(), name="review-list"),
    path("reviews/<int:review_id>/", pure_views.ReviewDetailView.as_view(), name="review-detail"),
    path("reviews/new/", pure_views.ReviewCreateView.as_view(), name="review-create"),
    path("reviews/<int:review_id>/edit/", pure_views.ReviewUpdateView.as_view(), name="review-update"),
    path("reviews/<int:review_id>/delete/", pure_views.ReviewDeleteView.as_view(), name="review-delete"),
    # profile
    path("users/<int:user_id>/", pure_views.ProfileView.as_view(), name="profile"),
    path("users/<int:user_id>/reviews/", pure_views.UserReviewListView.as_view(), name="user-review-list"),
    path("set-profile/", pure_views.ProfileSetView.as_view(), name="profile-set"),
    path("edit-profile/", pure_views.ProfileUpdateView.as_view(), name="profile-update"),
]

# api
urlpatterns += [
    path("api/", drf_views.IndexView.as_view()),
    path("api/reviews/", drf_views.ReviewListView.as_view()),
    path("api/reviews/<int:review_id>/", drf_views.ReviewDetailView.as_view()),
]