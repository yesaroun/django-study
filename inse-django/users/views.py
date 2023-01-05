from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import User

# Create your views here.
def show_user(request):
    users = get_object_or_404(User, 1)
    return HttpResponse(users.phone)

