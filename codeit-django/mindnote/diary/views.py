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


def page_create(request):
    if request.method == "POST":
        page_form = PageForm(request.POST)  # 입력된 데이터와 폼을 합쳐서 바인딩 폼 만들기
        new_post = page_form.save()  # 데이터 저장 및 생성된 데이터 모델 변환
        return redirect("page-detail", page_id=new_post.id)
    else:
        form = PageForm()
        return render(request, "diary/page_form.html", {"form": form})
