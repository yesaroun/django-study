from django.contrib import admin
from .models import Feed, Tag

# Register your models here.
@admin.register(Feed)
class FeedsAdmin(admin.ModelAdmin):
    list_display=("content","like", "user", "created", "updated")
    list_fileter=("content",)

@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    pass