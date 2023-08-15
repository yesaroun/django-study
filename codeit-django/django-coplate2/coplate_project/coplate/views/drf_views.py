from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from coplate.serializers import (
    ReviewSerializer,
    ReviewListSerializer,
    ReviewDetailSerializer,
)
from coplate.models import Review
from coplate.paginations import ReviewListPagination


class IndexView(APIView):

    @swagger_auto_schema(
        operation_description="List latest reviews",
        responses={200: ReviewSerializer(many=True)},
    )
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
    parser_classes = (MultiPartParser,)
    pagination_class = ReviewListPagination

    @swagger_auto_schema(
        operation_description="List reviews",
        responses={200: ReviewListSerializer(many=True)},
    )
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

    @swagger_auto_schema(
        operation_description="Create a new review",
        request_body=ReviewSerializer,
        responses={201: ReviewSerializer()},
    )
    def post(self, request, format=None):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailView(APIView):

    @swagger_auto_schema(
        operation_description="Retrieve a review",
        responses={200: ReviewDetailSerializer()},
    )
    def get(self, request, review_id, format=None):
        try:
            review = Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ReviewDetailSerializer(review)
        return Response(serializer.data)
