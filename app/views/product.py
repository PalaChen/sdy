from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from reposition import models
from utils.menu import get_cate_dic

cate_dic = get_cate_dic()
result_dict = {'status': 200, 'message': None, 'data': None, 'url': None}
status = {
    200: '正常',
    801: '用户不存在',
}


def index(req, id):
    is_login = req.session.get('is_login')
    user_info = req.session.get('user_info')
    product_obj = models.Products.objects.filter(id=id).first()
    service = models.ProductService.objects.filter(id=product_obj.p_service_id).first()
    service_obj = models.ProductService.objects.filter(root_id=service.root_id).all()
    city_obj = models.RegionalManagement.objects.all()
    nav_list = models.IndexNav.objects.order_by('-weight').values('name', 'url')[0:6]
    return render(req, 'product/index2.html', {'product_obj': product_obj,
                                               'cate_dic': cate_dic,
                                               'nav_list': nav_list,
                                               'is_login': is_login,
                                               'user_info': user_info,
                                               'city_obj': city_obj,
                                               'service_obj': service_obj})


def p_c_index(req, id):
    product_obj = models.Products.objects.filter(p_category_id=id).first()
    # service_obj = models.ProductService.objects.filter(category_id=id).all()
    # nav_list = models.IndexNav.objects.order_by('-weight').values('name', 'url')[0:6]
    return redirect('product_index', product_obj.id)
    # return render(req, 'product/index.html', {'product_obj': product_obj,
    #                                           'cate_dic': cate_dic,
    #                                           'nav_list': nav_list,
    #                                           'is_login': is_login,
    #                                           'service_obj': service_obj})


def buy(request):
    if request.method == 'GET':
        user_info = request.session.get('user_info')
        if user_info:
            id = request.GET.get('pid')

            product_obj = models.Products.objects.filter(id=id).first()
            if product_obj:
                result_dict['url'] = '/cart.html?pid={}'.format(id)
        else:
            result_dict['status'] = 801

        return JsonResponse(result_dict)


def get_city(request):
    if request.method == 'GET':
        city_obj = models.RegionalManagement.objects.values_list('code', 'name').order_by('id')
        city_dict = {}
        for code, name in city_obj:
            city_dict.update({code: name})

    return JsonResponse(city_dict)


from django import conf
import os


def get_town(request, code):
    base_dir = conf.settings.BASE_DIR

    file_path = base_dir + r'\static\town\{}.json'.format(str(code))
    print(file_path)
    # file_path =r'I:\django\sdy_new\static\town\440606.json'

    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read()
        print(data)
    return HttpResponse(data)
