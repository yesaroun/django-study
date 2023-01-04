from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    # class UserAdmin(admin.ModelAdmin):
    # list_display = ("nickname", "phone", "is_business", "gender", "profileIntroduce", "sns" )     # 이 조건들 보여줌
    # list_filter = ("is_business", )     # 필터 기능
    # search_fields = ("nickname", "phone" )      # 닉네임 기준 검색 기능
    # pass

    fieldsets = (
        ("Profile", {
            "fields": ("password", "email", "is_business"),
            "classes": ("wide",),
            },
        ),
        # ("Permissions", {
        #     "fields": (
        #         "is_active",
        #         "is_staff",
        #         "is_superuser",
        #         "user_permissions",
        #         ),
        #     "classes": ("collapse",),   # 이건 접었다가 폈다하는 기능
        #     },
        # ),
        # ("Important Dates", {
        #     "fields": ("last_login", "date_joined"),
        #     "classes": ("collapse",),
        #     },
        # ),
    )

    list_display = ("username", "email", "is_business")
