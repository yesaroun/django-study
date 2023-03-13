from rest_framework import serializers


class CategorySerializers(serializers.Serializer):
    name = serializers.CharField(
        max_length=50,
        required=True,
    )
