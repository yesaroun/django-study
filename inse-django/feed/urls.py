from django.urls import path
from . import views

urlpatterns = [
    path("", views.show_feed),
    # path("<int:feed_id>", views.one_feed),      # feeds/1
    path("all", views.all_feed)     # feeds/all
]