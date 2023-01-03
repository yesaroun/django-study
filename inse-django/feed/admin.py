from django.contrib import admin
from .models import Feed

@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ("img", "like", "content", )
    # search_fields = ("content", )

