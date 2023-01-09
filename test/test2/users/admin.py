from .models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # fields = ("email", "password", "name", "is_business")
    fieldsets = (
        ("Profile", {
                "fields": ("password", "name", "email", "is_business", "gender"),
                "classes": ("wide",),
            },
        ) ,
        ("Permissions", {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                ),
            },
        ) ,
        ("Important Dates", {
                "fields": ("last_login", "date_joined"),
                "classes": ("collapse",),
            },
        ),
    )

    list_display = ("username", "email", "name", "is_business",)