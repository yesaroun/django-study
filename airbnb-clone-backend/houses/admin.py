from django.contrib import admin
from .models import House


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):

    """house 관련 admin 세팅"""

    list_display: tuple = ("name", "price_per_night", "address", "pets_allowed")
    list_filter: tuple = ("price_per_night", "pets_allowed")
    search_fields: tuple = ("address",)
