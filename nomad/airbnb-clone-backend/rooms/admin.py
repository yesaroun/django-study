from django.contrib import admin
from rooms.models import Room, Amenity


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    pass
