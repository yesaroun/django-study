from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT

from drf_yasg.utils import swagger_auto_schema

from experiences.models import Perk
from experiences.serializers import PerkSerializer


class Perks(APIView):
    @swagger_auto_schema(
        operation_description="Get the list of all perks",
        responses={200: PerkSerializer(many=True)}
    )
    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new perk",
        request_body=PerkSerializer,
        responses={201: PerkSerializer}
    )
    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):
    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    @swagger_auto_schema(
        operation_description="Get a specific perk by ID",
        responses={200: PerkSerializer}
    )
    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a specific perk by ID",
        request_body=PerkSerializer,
        responses={200: PerkSerializer}
    )
    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk, data=request.data, partial=True)
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(PerkSerializer(updated_perk).data)
        else:
            return Response(serializer.errors)

    @swagger_auto_schema(
        operation_description="Delete a specific perk by ID",
        responses={204: "No Content"}
    )
    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)
