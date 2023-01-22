from django.shortcuts import render
from .models import Photo
from django.shortcuts import render, get_object_or_404


def photo_list(request):
    photos = Photo.objects.all()
    return render(request, 'photo/photo_list.html', {'photos': photos})


def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'photo/photo_detail.html', {'photo': photo})