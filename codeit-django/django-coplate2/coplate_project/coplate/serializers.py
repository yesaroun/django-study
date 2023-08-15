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


class ReviewUpdateSerializer(serializers.ModelSerializer):
    rating = serializers.ChoiceField(
        choices=Review.RATING_CHOICES,
    )

    class Meta:
        model = Review
        fields = (
            "title",
            "restaurant_name",
            "restaurant_link",
            "rating",
            "image1",
            "image2",
            "image3",
            "content",
        )
