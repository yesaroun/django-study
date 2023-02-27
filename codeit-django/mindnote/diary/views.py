from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.generic import CreateView, ListView, DeleteView
from django.urls import reverse
from .models import Page
from .forms import PageForm


# def page_list(request):
#     object_list = Page.objects.all()
#     paginator = Paginator(object_list, 8)
#     curr_page_num = request.GET.get("page")
#     if curr_page_num is None:
#         curr_page_num = 1
#     page = paginator.page(curr_page_num)
#     return render(request, "diary/page_list.html", {"page": page})
class PageListView(ListView):
    model = Page
    template_name = "diary/page_list.html"
    ordering = ["-dt_created"]
    paginate_by = 8
    page_kwarg = "page"


# def page_detail(request, page_id):
#     object = Page.objects.get(id=page_id)
#     return render(request, "diary/page_detail.html", {"object": object})
class PageDetailView(DeleteView):
    model = Page
    template_name = "diary/page_detail.html"
    pk_url_kwarg = "page_id"


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


# def page_create(request):
#
#     if request.method == "POST":
#         form = PageForm(request.POST)  # form : 입력된 데이터가 들어있는 바인딩 폼
#         if form.is_valid():
#             new_page = form.save()
#             return redirect("page-detail", page_id=new_page.id)
#     else:
#         form = PageForm()  # form :비어 있는 폼
#
#     return render(request, "diary/page_form.html", {"form": form})
class PageCreateView(CreateView):
    model = Page
    form_class = PageForm
    template_name = "diary/page_form.html"

    def get_success_url(self):
        # self.object는 이 CreateView에서 새로 생성한 데이터 모델
        return reverse("page-detail", kwargs={"page_id": self.object.id})


def page_update(request, page_id):
    object = Page.objects.get(id=page_id)
    if request.method == "POST":
        form = PageForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            return redirect("page-detail", page_id=object.id)
    else:
        form = PageForm(instance=object)
    return render(request, "diary/page_form.html", {"form": form})


def page_delete(request, page_id):
    object = Page.objects.get(id=page_id)
    if request.method == "POST":
        object.delete()
        return redirect("page-list")
    else:
        return render(request, "diary/page_confirm_delete.html", {"object": object})


def index(request):
    return render(request, "diary/index.html")
