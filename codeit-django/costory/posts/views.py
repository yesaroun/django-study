from django.shortcuts import render
from .models import Post
from .forms import PostForm


def post_list(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, 'posts/post_list.html', context)


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    context = {"post": post}
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    post_form = PostForm()
    return render(request, 'posts/post_form.html', {'form': post_form})