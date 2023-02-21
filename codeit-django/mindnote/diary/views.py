from django.shortcuts import render
from .models import Page
from .forms import PageForm


def page_list(request):
    object_list = Page.objects.all()
    return render(request, "diary/page_list.html", {"object_list": object_list})


def page_detail(request, page_id):
    object = Page.objects.get(id=page_id)
    return render(request, "diary/page_detail.html", {"object": object})


def info(request):
    return render(request, "diary/info.html")


def page_create(request):
    form = PageForm()
    return render(request, "diary/page_form.html", {"form": form})
