from django.contrib import admin
from .models import User

@admin.register(User)   # UserAdmin에 등록할 Model 지정(Decorator)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Profile Info", {
            "fields": ("email", "password", "is_business"),
            "classes": ("wide",),
            },
        ),
        ("Permissions", {
            "fields":{
                "is_active",
                "is_staff"
            }
            }
        )
    )


class CustomUserAdmin(UserAdmin):
    fieldsets = None
    fields = ("email", "password", "name")