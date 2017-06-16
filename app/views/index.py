from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from app import forms
from reposition import models, model_query, model_update, model_add
from utils.check_code import create_validate_code
import io
import datetime
from django.db.models import Q
from utils.menu import get_cate_list, shop_number


# city_obj = models.RegionalManagement.objects.filter(Q(r_code__isnull=False)).all()
# current_city = '佛山市'
# request.session['global_variale'] = {'city_obj': city_obj, 'current_city': current_city}


def index(request):
    user_info = shop_number(request)
    default_city = request.session.get('default_city')
    title = '盛德业,注册公司,代理记账,商标注册,个人社保,企业社保,创业法律服务'
    is_login = None
    if request.method == 'GET':
        bxSlider = models.Bxslider.objects.filter(status=1).order_by('weight').all()
        articles_list = models.Articles.objects.order_by('-ctime').values('id', 'category_id', 'title')[0:6]
        articles_images_obj = models.Articles.objects.order_by('-ctime')[6:10]
        nav_list = models.IndexNav.objects.order_by('-weight').values('name', 'url', 'ishot')[0:7]
        city_obj = models.RegionalManagement.objects.filter(Q(r_code__isnull=False)).all()
        packages_obj = models.Package.objects.filter(status=1, area_id=default_city['area_id']).order_by('weight')[0:3]
        # 推荐产品列表
        recommend_obj = models.Products.objects.filter(p_top=1).order_by('-p_ctime')[0:9]
        cate_list = get_cate_list()
        cookie = request.COOKIES
        is_login = request.session.get('is_login')
        from django.template import loader
        # content = loader.render_to_string('user/user_index.html')
        # print(content)
        d = {'bxSlider': bxSlider, 'cate_list': cate_list,
             'cookie': cookie, 'is_login': is_login,
             'nav_list': nav_list, 'articles_list': articles_list,
             'user_info': user_info, 'city_obj': city_obj,
             'articles_images_obj': articles_images_obj,
             'default_city': default_city, 'title': title,
             'recommend_obj': recommend_obj, 'packages_obj': packages_obj,}
        return render(request, 'index.html', d)


# 切换城市
def switch_city(request, city_id):
    city_obj = models.RegionalManagement.objects.filter(id=city_id).first()
    area_obj = models.RegionalManagement.objects.filter(p_code=city_obj.code).first()
    if city_obj:
        request.session['default_city'] = {'city_id': city_obj.id, 'city': city_obj.name,
                                           'area_id': area_obj.id}
    return redirect('web_index')
