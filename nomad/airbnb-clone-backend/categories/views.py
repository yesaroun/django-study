from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from drf_yasg.utils import swagger_auto_schema

from categories.models import Category
from categories.serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
