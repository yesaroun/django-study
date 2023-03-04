from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Movie, Actor
from .serializers import MovieSerializer, ActorSerializer


@api_view(["GET"])
def movie_list(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=200)


@api_view(["GET"])
def actor_list(request):
    actors = Actor.objects.all()
    serializer = ActorSerializer(actors, many=True)
    return Response(serializer.data, status=200)
