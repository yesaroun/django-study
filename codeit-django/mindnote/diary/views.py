from django.shortcuts import render, redirect
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


# def page_create(request):
#     if request.method == "POST":
#         form = PageForm(request.POST)  # form : 입력된 데이터가 들어있는 바인딩 폼
#         if form.is_valid():
#             new_page = form.save()
#             return redirect("page-detail", page_id=new_page.id)
#         else:  # 이 데이터가 유효하지 않은 경우
#             return render(request, "diary/page_form.html", {"form": form})
#     else:
#         form = PageForm()  # form :비어 있는 폼
#         return render(request, "diary/page_form.html", {"form": form})


def page_create(request):

    if request.method == "POST":
        form = PageForm(request.POST)  # form : 입력된 데이터가 들어있는 바인딩 폼
        if form.is_valid():
            new_page = form.save()
            return redirect("page-detail", page_id=new_page.id)
    else:
        form = PageForm()  # form :비어 있는 폼

    return render(request, "diary/page_form.html", {"form": form})
