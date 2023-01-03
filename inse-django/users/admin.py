from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("nickname", "phone", "is_business", "gender", "profileIntroduce", )     # 이 조건들 보여줌
    list_filter = ("is_business", )     # 필터 기능
    search_fields = ("nickname", "phone" )      # 닉네임 기준 검색 기능
