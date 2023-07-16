from rest_framework import serializers
from coplate.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class ReviewListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.nickname")

    class Meta:
        model = Review
        fields = (
            "id",
            "title",
            "restaurant_name",
            "rating",
            "image1",
            "dt_updated",
            "author_name",
        )


class ReviewDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.nickname")
    
    class Meta:
        model = Review
        fields = "__all__"
        