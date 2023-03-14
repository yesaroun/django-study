from django.db.models import QuerySet
from rest_framework.serializers import ListSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Amenity
from .serializers import AmenitySerializer
from typing import List


class Amenities(APIView):
    def get(self, request) -> Response:
        print(type(self), ": self")
        all_amenities: QuerySet[Amenity] = Amenity.objects.all()
        serializer: List[AmenitySerializer] = AmenitySerializer(
            all_amenities, many=True
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get(self, request, pk):
        pass

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        pass
