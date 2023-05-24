from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DeleteView
from allauth.account.views import PasswordChangeView
from .models import Post


class IndexView(ListView):
    model = Post
    template_name = "podomarket/index.html"
    context_object_name = "posts"
    paginate_by = 8
    ordering = ["-dt_updated"]


class PostDetailView(DeleteView):
    model = Post
    template_name = "podomarket/post_detail.html"
    pk_url_kwarg = "post_id"


class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self) -> str:
        return reverse("index")
