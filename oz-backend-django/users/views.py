from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework.status import 
from rest_framework.permissions import IsAuthenticated
from .serializers import MyInfoUserSerializer

class MyInfo(APIView):
    # read
    def get(self, request):
        user = request.user
        serializer = MyInfoUserSerializer(user)
        return Response(serializer.data)

    # update
    def put(self, request):
        user = request.user
        serializer = MyInfoUserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            user = serializer.save()
            serializer = MyInfoUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)