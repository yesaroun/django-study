from rest_framework import serializers
from .models import Booking


class PublicBookingSerializer(serializers.ModelSerializer):
    """
    모두가 볼 수 있는 Booking serializer
    """

    class Meta:
        model = Booking
        fields = (
            "pk",
            "room",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )


"""
집 주인을 위한 Booking serializer
"""
