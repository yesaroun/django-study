from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

# Create your views here.
def index_view(request):
    return HttpResponse('<h1>코스토랑 오픈!<h1>')

def index(request):
    today = str(datetime.now().date())
    context = {"date":today}
    return render(request, 'menus/index.html', context=context)

def detail(request, menu):
    return render(request, 'menus/detail.html')