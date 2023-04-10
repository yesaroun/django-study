from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from medias.serializers import PhotoSerializer
from categories.serializers import CategorySerializer
from reviews.serializers import ReviewSerializer
from wishlists.models import WishList


class AmenitySerializer(ModelSerializer):
    """
    Amenity를 위한 Serializer
    """

    class Meta:
        model = Amenity
        fields = "name", "description"


class RoomDetailSerializer(ModelSerializer):
    """
    Room detail을 위한 Serailizer
    """

    owner = TinyUserSerializer(
        read_only=True,
    )
    amenities = AmenitySerializer(
        read_only=True,
        many=True,
    )
    category = CategorySerializer(
        read_only=True,
    )
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room) -> float:
        """
        Room 인스턴스의 평가 평균 계산
        """
        return room.rating()

    def get_is_owner(self, room) -> bool:
        """
        Room 인스턴스의 주인인지 확인
        """
        request = self.context["request"]
        return room.owner == request.user

    # def create(self, validated_data):
    #     return Room.objects.create(**validated_data)

    def get_is_liked(self, room) -> bool:
        """
        유저가 Room 인스턴스에 좋아요를 눌렀는지 확인
        """
        request = self.context["request"]
        return WishList.objects.filter(
            user=request.user,
            rooms__pk=room.pk,
        ).exists()


class RoomListSerializer(ModelSerializer):
    """
    Room List를 위한 Serialzier
    """

    rating = serializers.SerializerMethodField
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
        )

    def get_rating(self, room) -> float:
        """
        Room 인스턴스의 평점 평균
        """
        return room.rating()

    def get_is_owner(self, room) -> bool:
        """
        유저가 Room 인스턴스의 주인인지 확인
        """
        request = self.context["request"]
        return room.owner == request.user
