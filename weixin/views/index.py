from django.shortcuts import render, redirect
from utils.menu import get_cate_list, user_info
from reposition import models
from django.db.models import Q

title = {'city': '地区选择'}


def switche_city(request):
    city_obj = models.RegionalManagement.objects.filter(Q(r_code__isnull=False)).all()
    context = {
        'city_obj': city_obj,
        'title': title['city']
    }
    return render(request, 'wap/city.html', context)


def index(request):
    return render(request, 'wap/index.html')


def login(request):
    return render(request, 'wap/login.html')


def register(request):
    return render(request, 'wap/register.html')


def mycenter(request):
    return render(request, 'wap/mycenter.html')


def findpass(request):
    return render(request, 'wap/findpass.html')
