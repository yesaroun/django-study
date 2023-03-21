from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = "name", "description"


class RoomDetailSerializer(ModelSerializer):

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

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        return room.rating()

    # def create(self, validated_data):
    #     return Room.objects.create(**validated_data)


class RoomListSerializer(ModelSerializer):

    rating = serializers.SerializerMethodField

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
        )

    def get_rating(self, room):
        return room.rating()
