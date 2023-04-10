from rest_framework.serializers import ModelSerializer
from rooms.serializers import RoomListSerializer
from .models import WishList


class WishlistSerializer(ModelSerializer):
    """
    Wishlist 시리얼라이저
    """

    rooms = RoomListSerializer(
        many=True,
        read_only=True,  # post 할때는 room의 정보 입력하지 않도록 read_only
    )

    class Meta:
        model = WishList
        fields = (
            "pk",
            "name",
            "rooms",
        )
