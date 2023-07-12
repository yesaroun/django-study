from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from coplate.serializers import (
    ReviewSerializer,
    ReviewListSerializer,
    ReviewDetailSerializer,
)
from coplate.models import Review
from coplate.paginations import ReviewListPagination


class IndexView(APIView):
    def get(self, request, format=None):
        try:
            latest_reviews = Review.objects.all()[:4]
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        serializer = ReviewSerializer(latest_reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewListView(APIView):
    pagination_class = ReviewListPagination

    def get(self, request, format=None):
        try:
            reviews = Review.objects.all()
            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(reviews, request)
            serializer = ReviewListSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReviewDetailView(APIView):
    def get(self, request, review_id, format=None):
        try:
            review = Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ReviewDetailSerializer(review)
        return Response(serializer.data)
