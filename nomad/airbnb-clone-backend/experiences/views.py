from rest_framework.views import APIView
from rest_framework.response import Response

from experiences.models import Perk
from experiences.serializers import PerkSerializer


class Perks(APIView):
    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

