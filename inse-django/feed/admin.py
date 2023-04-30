from django.contrib import admin
from .models import Feed

@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ("imgs", "like", "content", "created", "updated")
    # search_fields = ("content", )

