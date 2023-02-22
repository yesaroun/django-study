from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm


def post_list(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "posts/post_list.html", context)


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    context = {"post": post}
    return render(request, "posts/post_detail.html", context)


def post_create(request):
    if request.method == "POST":
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            new_post = post_form.save()
            return redirect("post-detail", post_id=new_post.id)
    else:
        post_form = PostForm()
    return render(request, "posts/post_form.html", {"form": post_form})
