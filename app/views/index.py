from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from app import forms
from reposition import models, model_query, model_update, model_add
from utils.check_code import create_validate_code
import io
import datetime
from utils.menu import get_cate_dic


def index(req):
    user_info = req.session.get('user_info')
    is_login = None
    if req.method == 'GET':
        bxSlider = models.Bxslider.objects.filter(status=1).order_by('weight').all()
        articles_list = models.Articles.objects.order_by('-ctime').values('id', 'category_id', 'title')[0:9]
        nav_list = models.IndexNav.objects.order_by('-weight').values('name', 'url')[0:6]
        cate_dic = get_cate_dic()
        cookie = req.COOKIES
        is_login = req.session.get('is_login')

        return render(req, 'index.html', {'bxSlider': bxSlider, 'cate_dic': cate_dic,
                                          'cookie': cookie, 'is_login': is_login,
                                          'nav_list': nav_list, 'articles_list': articles_list,
                                          'user_info': user_info,})
