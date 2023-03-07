from rest_framework import serializers
from .models import Movie, Actor, Review


class MovieSerializer(serializers.ModelSerializer):
    movie_reviews = serializers.PrimaryKeyRelatedField(
        source="reviews", many=True, read_only=True
    )

    class Meta:
        model = Movie
        fields = [
            "id",
            "name",
            "movie_reviews",
            "opening_date",
            "running_time",
            "overview",
        ]


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["id", "name", "gender", "birth_date"]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "movie", "username", "star", "comment", "created"]
        extra_kwargs = {
            "movie": {"read_only": True},
        }
