from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from app import forms
from reposition import models, model_query, model_update, model_add
from utils.check_code import create_validate_code
import io
import datetime
from django.db.models import Q
from utils.menu import get_cate_dic


# city_obj = models.RegionalManagement.objects.filter(Q(r_code__isnull=False)).all()
# current_city = '佛山市'
# request.session['global_variale'] = {'city_obj': city_obj, 'current_city': current_city}


def index(req):
    user_info = req.session.get('user_info')
    default_city = req.session.get('default_city')
    title = '盛德业,注册公司,代理记账,商标注册,个人社保,企业社保,创业法律服务'
    is_login = None
    if req.method == 'GET':
        bxSlider = models.Bxslider.objects.filter(status=1).order_by('weight').all()
        articles_list = models.Articles.objects.order_by('-ctime').values('id', 'category_id', 'title')[0:9]
        nav_list = models.IndexNav.objects.order_by('-weight').values('name', 'url', 'ishot')[0:6]
        city_obj = models.RegionalManagement.objects.filter(Q(r_code__isnull=False)).all()
        recommend_obj = models.Products.objects.filter(p_top=1).order_by('-p_ctime')[0:8]
        cate_dic = get_cate_dic()
        cookie = req.COOKIES
        is_login = req.session.get('is_login')

        return render(req, 'index.html', {'bxSlider': bxSlider, 'cate_dic': cate_dic,
                                          'cookie': cookie, 'is_login': is_login,
                                          'nav_list': nav_list, 'articles_list': articles_list,
                                          'user_info': user_info, 'city_obj': city_obj,
                                          'default_city': default_city, 'title': title,
                                          'recommend_obj': recommend_obj})
