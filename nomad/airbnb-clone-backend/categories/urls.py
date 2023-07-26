from django.urls import path
from categories import views

urlpatterns = [
    path("", views.categories),
    path("<int:pk>", views.category),
]
