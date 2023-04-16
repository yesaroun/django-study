from django.utils import timezone
from rest_framework import serializers
from .models import Booking


class CreateRoomBookingSerializer(serializers.ModelSerializer):

    check_in = serializers.DateField()
    check_out = serializers.DateField()
    # 2) : 여기서는 날짜 필드가 맞는지 체크
    # 여기에서 검증하는 결과에 따라서 view의 valid가 동작하는 것이다.
    # 추가적인 검증이 필요하면 여기서 반영할 수 있다.
    # 3)으로 이동

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    # 3) validate 뒤에 _ 를 입력하고 validate 하고 싶은 field의 이름을 입력한다. 예를 들어 check_in
    # 특정 field의 validation을 customize하고 싶으면
    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        # 오늘 date만 받아옴
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        # 날짜 validation     views 4)로 이동
        return value

    # 5) 똑같이 작성
    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value


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
