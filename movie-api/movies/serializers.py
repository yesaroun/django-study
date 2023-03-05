from rest_framework import serializers
from .models import Movie, Actor


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "name", "opening_date", "running_time", "overview"]


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["id", "name", "gender", "birth_date"]
