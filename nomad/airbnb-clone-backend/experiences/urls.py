from django.urls import path 
from experiences.views import PerkDetail, Perks

urlpatterns = [
    path("perks/", Perk.as_view()),
    path("perks/<int:pk>", PerkDetail.as_view()),
]
