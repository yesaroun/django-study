from django.contrib import admin
from .models import House


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):

    """house 관련 admin 세팅"""

    fields = (
        "name",
        "address",
        ("price_per_night", "pets_allowed"),
    )
    list_display: tuple = ("name", "price_per_night", "address", "pets_allowed")
    list_filter: tuple = ("price_per_night", "pets_allowed")
    search_fields: tuple = ("address",)
    list_display_links = ("name", "address")
    list_editable = ("pets_allowed",)
