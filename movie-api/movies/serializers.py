from rest_framework import serializers
from .models import Movie, Actor, Review


class MovieSerializer(serializers.ModelSerializer):
    reviews = serializers.StringRelatedField(many=True)

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


class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = ["id", "movie", "username", "star", "comment", "created"]
