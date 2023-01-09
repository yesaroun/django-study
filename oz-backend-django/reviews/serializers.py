from rest_framework import serializers
from .models import Review

class FeedReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        # fields = "__all__"
        fields = ("id", "content", "like")