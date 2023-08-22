from django.db import transaction

from rest_framework.views import APIView
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
)
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)

from drf_yasg.utils import swagger_auto_schema

from rooms.serializers import (
    AmenitySerializer,
    RoomDetailSerializer,
    RoomListSerializer,
)
from rooms.models import Amenity, Room

from categories.models import Category


class Amenities(APIView):
    @swagger_auto_schema(
        operation_description="Get the list of all amenities",
        responses={200: AmenitySerializer(many=True)}
    )
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new amenity",
        request_body=AmenitySerializer,
        responses={201: AmenitySerializer}
    )
    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    @swagger_auto_schema(
        operation_description="Get a specific amenity by ID",
        responses={200: AmenitySerializer}
    )
    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a specific amenity by ID",
        request_body=AmenitySerializer,
        responses={200: AmenitySerializer}
    )
    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(
                AmenitySerializer(updated_amenity).data,
            )
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

    @swagger_auto_schema(
        operation_description="Delete a specific amenity by ID",
        responses={204: "No Content"}
    )
    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):
    @swagger_auto_schema(
        operation_description="Get the list of all rooms",
        responses={200: RoomListSerializer(many=True)}
    )
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new room",
        request_body=RoomDetailSerializer,
        responses={201: RoomDetailSerializer}
    )
    def post(self, request):
        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                category_pk = request.data.get("category")
                if not category_pk:
                    raise ParseError("Category is required.")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be 'rooms")
                except Category.DoesNotExist:
                    raise ParseError("Category not found")
                try:
                    with transaction.atomic():
                        room = serializer.save(owner=request.user, category=category)
                        amenities = request.data.get("amenities")
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)
                        serializer = RoomDetailSerializer(room)
                        return Response(serializer.data)
                except Exception:
                    raise ParseError("Amenity not found")
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    @swagger_auto_schema(
        operation_description="Get a specific room by ID",
        responses={200: RoomDetailSerializer}
    )
    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room)
        return Response(serializer.data)
