from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

# Create your views here.
def index_view(request):
    return HttpResponse('<h1>코스토랑 오픈!<h1>')

def index(requeest):
    today = str(datetime.now().date())
    context = {"date":today}
    return render(requeest, 'menus/index.html', context=context)