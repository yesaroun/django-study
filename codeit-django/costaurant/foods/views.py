from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime


def index(request):
    today = datetime.today().date()
    context = {"date":today}
    return render(request, 'foods/index.html', context=context)

def food_detail(request, food):  #넘어온 변수를 받아줄 두번째 파라미터 필요
    context = {"name":food}
    return render(request, 'foods/detail.html', context=context)