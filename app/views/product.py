from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import JsonResponse
from reposition import models
from utils.menu import get_cate_dic
from django.db.models import Q

cate_dic = get_cate_dic()

status = {
    200: '正常',
    801: '用户不存在',
}


def index(req, id):
    is_login = req.session.get('is_login')
    user_info = req.session.get('user_info')
    default_city = req.session.get('default_city')
    product_obj = models.Products.objects.filter(id=id, area_id=default_city['area_id']).first()
    if not product_obj:
        product_obj = get_object_or_404(models.Products, id=id)
        default_city = {'city_id': product_obj.city_id, 'city': product_obj.city.name, 'area_id': product_obj.area_id}
        req.session['default_city'] = default_city
    service = get_object_or_404(models.ProductService, id=product_obj.p_service_id)
    service_obj = models.ProductService.objects.filter(root_id=service.root_id).all()
    city_obj = models.RegionalManagement.objects.filter(Q(r_code__isnull=False)).all()
    nav_list = models.IndexNav.objects.order_by('-weight').values('name', 'url')[0:6]

    # 商品详情页左侧推信息
    category_obj = models.ProductCategory.objects.filter(Q(parent_id__gt=0)).all()
    products_obj = models.Products.objects.filter(area_id=default_city['area_id']).all()

    return render(req, 'product/index2.html', {'product_obj': product_obj,
                                               'cate_dic': cate_dic,
                                               'nav_list': nav_list,
                                               'is_login': is_login,
                                               'user_info': user_info,
                                               'city_obj': city_obj,
                                               'default_city': default_city,
                                               'category_obj': category_obj,
                                               'products_obj': products_obj,
                                               'service_obj': service_obj})


def p_c_index(request, id):
    default_city = request.session['default_city']
    product_obj = models.Products.objects.filter(p_category_id=id, area_id=default_city['area_id']).first()
    if product_obj:
        return redirect('product_index', product_obj.id)
    else:
        return redirect('web_index')


def buy(request):
    result_dict = {'status': 200, 'message': None, 'data': None, 'url': None}
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


# 获取当前产品对应的城市信息
def product_city(request):
    result_dict = {'status': 200, 'message': None, 'data': None, 'url': None}
    id = request.GET.get('nid')
    product_obj = models.Products.objects.filter(id=id).first()
    if product_obj:
        result_dict['message'] = {'city': product_obj.city.name, 'area': product_obj.area.name}
    else:
        result_dict['status'] = False
    return JsonResponse(result_dict)
    # if product_obj:
    #     result_dict['message']={'city':product_obj.city_id.name}


# 通过服务分类id获取产品信息
def get_cat_product(request):
    result_dict = {'status': 200, 'message': None, 'data': None, 'url': None}
    if request.method == 'GET':
        nid = request.GET.get('nid')
        default_city = request.session['default_city']
        product_obj = models.Products.objects.filter(p_service_id=nid,
                                                     area_id=default_city['area_id']).values('id').first()
        if product_obj:
            result_dict['data'] = product_obj['id']
            return JsonResponse(result_dict)

    result_dict['status'] = 404
    return JsonResponse(result_dict)


# 通过地区获取对应的产品信息，并且修改默认城市信息
def get_product(request):
    # print(1111111)
    result_dict = {'status': 200, 'message': None, 'data': None, 'url': None}
    if request.method == 'GET':
        area_code = request.GET.get('area')
        nid = request.GET.get('nid')
        area_obj = models.RegionalManagement.objects.filter(code=area_code).first()
        default_city = request.session['default_city']
        if area_obj.id != default_city['area_id']:
            city_obj = models.RegionalManagement.objects.filter(code=area_obj.p_code).first()
            default_city["area_id"] = area_obj.id
            default_city["city_id"] = city_obj.id
            default_city["city"] = city_obj.name
            request.session['default_city'] = default_city
        product_obj = models.Products.objects.filter(p_service_id=nid,
                                                     area_id=area_obj.id).values('id').first()

        if product_obj:
            result_dict['data'] = product_obj['id']
            return JsonResponse(result_dict)

    result_dict['status'] = 404
    return JsonResponse(result_dict)


# 获取产品下面地区各个城市对应关系
def get_city(request):
    result_dict = {'status': 200, 'message': None, 'data': None, 'url': None}
    if request.method == 'GET':
        region_obj = models.RegionalManagement.objects.all()
        # area_obj = models.Products.objects.values('area__name','area__code','area__code').distinct()
        province_dict = []
        city_dict = []
        area_dict = []
        for line in region_obj:
            if not line.r_code and not line.p_code:
                province_dict.append({'id': line.code, 'name': line.name,})
            elif line.r_code:
                city_dict.append({'id': line.code, 'name': line.name, 'pid': line.r_code})
            elif line.p_code:
                area_dict.append({'id': line.code, 'name': line.name, 'pid': line.p_code})

        result_dict['message'] = {'province': province_dict, 'city': city_dict, 'area': area_dict}
    # print(result_dict)
    return JsonResponse(result_dict)


from django import conf
import os


def get_town(request, code):
    base_dir = conf.settings.BASE_DIR

    file_path = base_dir + r'\static\town\{}.json'.format(str(code))
    # print(file_path)
    # file_path =r'I:\django\sdy_new\static\town\440606.json'

    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read()
        print(data)
    return HttpResponse(data)
