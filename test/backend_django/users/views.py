from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response


class Users(APIView):
    def get(self, request):
        users = User.objects.all()          # objects
        serializer = UserSerializer(users, many=True)  # json

        return Response(serializer.data)

