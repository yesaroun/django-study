from rest_framework import serializers
from .models import Movie, Actor


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "name", "opening_date", "running_time", "overview"]


class ActorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    gender = serializers.CharField()
    birth_date = serializers.DateField()

    def create(self, validated_data):
        return Actor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.birth_date = validated_data.get("birth_date", instance.birth_date)
        instance.save()
        return instance
