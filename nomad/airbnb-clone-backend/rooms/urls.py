from django.urls import path

from rooms import views

urlpatterns = [
    path("amenities/", views.Amenities.as_view()),
    path("amenities/<int:pk>", views.AmenityDetail.as_view()),
]
