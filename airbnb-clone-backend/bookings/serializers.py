from django.utils import timezone
from rest_framework import serializers
from .models import Booking


class CreateRoomBookingSerializer(serializers.ModelSerializer):

    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value

    def validate(self, data):
        # validation 1 : check_in 날짜가 check_out보다 클 경우
        if data["check_out"] <= data["check_in"]:
            raise serializers.ValidationError(
                "Check in should be smaller than check out."
            )
        # validation2 : booking을 저장하기 전에 이 날짜 사이에 다른 booking이 있는지 확인
        if Booking.objects.filter(
            check_in__lte=data["check_out"],
            check_out__gte=data["check_in"],
        ).exists():
            raise serializers.ValidationError(
                "Those (or some) of those dates are already taken."
            )
        return data


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
