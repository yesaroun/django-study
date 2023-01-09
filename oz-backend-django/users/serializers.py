from rest_framework.serializers import ModelSerializer
from .models import User

# Feed에서 노출시킬 User Serializer
class FeedUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "is_business")

# MyInfo User Serialzier
class MyInfoUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ("password", "is_superuser", "is_staff", "is_active",
                    "first_name", "last_name")

        # fields = "__all__" # Model의 전체 field 가져옴
        # fields = ("nickname", "email") # 원하는 특정 field만 가져옴
        # exclude = ("password",) # 특정 field 제외 가능