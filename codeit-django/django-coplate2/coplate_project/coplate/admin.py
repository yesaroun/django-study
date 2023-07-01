from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Review, Comment, Like

UserAdmin.fieldsets += (
    (
        "Custom fields",
        {
            "fields": (
                "nickname",
                "profile_pic",
                "intro",
                "following",
            )
        },
    ),
)

admin.site.register(User, UserAdmin)

admin.site.register(Review)

admin.site.register(Comment)

admin.site.register(Like)
