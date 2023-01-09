from django.contrib import admin
from .models import User

# Register your models here.
# @admin.register(User) # UsersAdmin에 등록할 Model 지정 (Decorator)
# class UsersAdmin(admin.ModelAdmin): # ModelAdmin을 상속
# 	# pass
#     list_display = ["name", "age", "sex", "is_business"]
#     list_filter= ["sex", "is_business"]
#     search_fields = ["name"]

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
        ),
        ("Permissions",{
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                ),
            },
        ),
        ("Important Dates", {
                "fields": ("last_login", "date_joined"),
                "classes": ("collapse",),
            },
        ),
    )

    list_display = ("username", "email", "name", "is_business", "gender")