from django.shortcuts import render
from django.http import HttpResponse

def show_review(request):
    return HttpResponse("hi")