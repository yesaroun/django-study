from rest_framework import serializers
from .models import Movie, Actor, Review


class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = ["id", "movie", "username", "star", "comment", "created"]


class MovieSerializer(serializers.ModelSerializer):
    # Nested Serializer를 사용하려면
    # MoviewSerializer 선언 전에 ReviewSerializer가 선언되어야 함.
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
            "id",
            "name",
            "reviews",
            "opening_date",
            "running_time",
            "overview",
        ]


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["id", "name", "gender", "birth_date"]
