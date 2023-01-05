from django.contrib import admin
from feed.models import Feed


@admin.register(Feed)
class FreedAdmin(admin.ModelAdmin):
    list_display = ("img", "like", "content", "created", "updated")