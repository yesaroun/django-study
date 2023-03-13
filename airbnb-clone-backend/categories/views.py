from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializers


@api_view(["GET", "POST"])
def categories(request):

    if request.method == "GET":
        all_categories = Category.objects.all()
        serializer = CategorySerializers(all_categories, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CategorySerializers(data=request.data)
        if serializer.is_valid():
            return Response({"created": True})
        else:
            return Response(serializer.errors)
    # {"name": "from DRF"}


@api_view()
def category(request, pk):
    category = Category.objects.get(pk=pk)
    serializer = CategorySerializers(category)
    return Response(serializer.data)
