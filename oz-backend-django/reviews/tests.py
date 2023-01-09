from django.shortcuts import render
from django.http import HttpResponse

def show_reivew(request):
    return HttpResponse("This is Review page")