from .models import Reveiw
from django.contrib import admin
from django.db.models import QuerySet


class WordFilter(admin.SimpleListFilter):

    title = "Filter by worlds"

    parameter_name = "potato"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]

    def queryset(self, request, reviews: QuerySet):
        word = self.value()
        if word:
            return reviews.filter(payload__contains=word)
        else:
            return reviews


@admin.register(Reveiw)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "__str__",
        "payload",
    )
    list_filter = (
        WordFilter,
        "rating",
        "user__is_host",
        "room__category",
        "room__pet_friendly",
    )
