# coding:utf-8
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import JsonResponse
from reposition import models
from utils.menu import get_cate_list
from utils.menu import user_info
from django.db.models import Q

status = {
    200: '正常',
    801: '用户不存在',
}


def index(req, id):
    """
    产品页面
    :param req:
    :param id: 产品id
    :return:
    """
    is_login = req.session.get('is_login')
    user_dict = user_info(req)
    default_city = req.session.get('default_city')
    product_obj = models.Products.objects.filter(id=id, area_id=default_city['area_id']).first()
    if not product_obj:
        product_obj = get_object_or_404(models.Products, id=id)
        default_city = {'city_id': product_obj.city_id, 'city': product_obj.city.name, 'area_id': product_obj.area_id}
        req.session['default_city'] = default_city

    if product_obj.p_service:
        service = get_object_or_404(models.ProductService, id=product_obj.p_service_id)
        service_obj = models.ProductService.objects.filter(root_id=service.root_id).all()
    else:
        service_obj = ''
    # 城市列表
    city_obj = models.RegionalManagement.objects.filter(Q(r_code__isnull=False)).all()
    # 导航
    nav_list = models.IndexNav.objects.order_by('-weight').values('name', 'url', 'ishot')[0:7]
    cate_list = get_cate_list()
    # 商品详情页左侧推信息
    category_obj = models.ProductCategory.objects.filter(Q(parent_id__gt=0)).all()
    products_obj = models.Products.objects.filter(area_id=default_city['area_id']).all()
    return render(req, 'product/index2.html', {'product_obj': product_obj,
                                               'cate_list': cate_list,
                                               'nav_list': nav_list,
                                               'is_login': is_login,
                                               'user_info': user_dict,
                                               'city_obj': city_obj,
                                               'default_city': default_city,
                                               'category_obj': category_obj,
                                               'products_obj': products_obj,
                                               'service_obj': service_obj})


def pacakage_index(request, id):
    is_login = request.session.get('is_login')
    user_dict = user_info(request)
    default_city = request.session['default_city']
    city_obj = models.RegionalManagement.objects.filter(Q(r_code__isnull=False)).all()
    package_obj = models.Package.objects.filter(id=id, status=1, area_id=default_city['area_id']).first()
    nav_list = models.IndexNav.objects.order_by('-weight').values('name', 'url', 'ishot')[0:7]
    # 商品详情页左侧推信息
    category_obj = models.ProductCategory.objects.filter(Q(parent_id__gt=0)).all()
    products_obj = models.Products.objects.filter(area_id=default_city['area_id']).all()
    d = {
        'package_obj': package_obj,
        'nav_list': nav_list,
        'is_login': is_login,
        'user_info': user_dict,
        'city_obj': city_obj,
        'default_city': default_city,
        'category_obj': category_obj,
        'products_obj': products_obj,
    }
    return render(request, 'product/package_index.html', d)


def p_c_index(request, id):
    default_city = request.session['default_city']
    if default_city['area_id']:
        product_obj = models.Products.objects.filter(p_category_id=id, area_id=default_city['area_id']).first()
    else:
        product_obj = models.Products.objects.filter(p_category_id=id).first()
    if product_obj:
        return redirect('product_index', product_obj.id)
    else:
        return redirect('web_index')


def buy(request):
    """
    用户点击购买按钮，如果该商品有套餐，则显示套餐页面详情
    :param request:
    :return:
    """
    result_dict = {'status': 200, 'message': None, 'data': None, 'url': None}
    if request.method == 'GET':
        user_dict = user_info(request)
        # 判断用户信息是否存在
        if user_dict:
            pid = request.GET.get('pid')
            # 判断pid是否存在
            if pid:
                # 产品
                product_obj = models.Products.objects.filter(id=pid).first()
                if product_obj:
                    # 产品对应的套餐
                    packages_obj = models.Product2Package.objects.filter(product_id=pid).all()
                    if packages_obj:
                        result_dict['data'] = True
                        result_dict['url'] = '/product/package/ppid/{}.html'.format(pid)
                    else:
                        result_dict['data'] = False
                        result_dict['url'] = '/package/{}.html'.format(pid)
                else:
                    result_dict['data'] = False
                    result_dict['url'] = '非法请求'
            else:
                result_dict['status'] = 401
                result_dict['error_message'] = '该请求属于非法请求'

        else:
            result_dict['status'] = 801
            result_dict['error_message'] = '请先登录账号'
    else:
        result_dict['status'] = 401
        result_dict['error_message'] = '该请求属于非法请求'
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


def product_package(request, product_id):
    """
    套餐页面显示
    :param request:
    :param product_id:产品id
    :return:
    """
    pacakage_list = []
    sort = 0
    # 产品对应的套餐
    packages_obj = models.Product2Package.objects.filter(product_id=product_id).all()
    if packages_obj:
        for package_obj in packages_obj:
            package2products_obj = models.Package2Product.objects.filter(package=package_obj.package).all()
            product_list = []
            for package2product in package2products_obj:
                product_dict = {'p_name': package2product.product.p_name,
                                'p_price': package2product.product.p_price}
                product_list.append(product_dict)
            # 如果套餐中已经包含商品，则添加入购物车
            pacakage_dict = {'sort': sort,
                             'name': package_obj.package.name,
                             'info': {'id': package_obj.package.id,
                                      'description': package_obj.package.dscription,
                                      'cprice': package_obj.package.cprice,
                                      'original_price': package_obj.package.original_price,
                                      "product": product_list}}
            pacakage_list.append(pacakage_dict)
            sort += 1
        return render(request, 'product/package.html', {'pacakage_list': pacakage_list,
                                                        'product_id': product_id, })


def pp_buy(request, id):
    user_dict = user_info(request)
    default_city = request.session.get('default_city')
    city_obj = models.RegionalManagement.objects.filter(Q(r_code__isnull=False)).all()
    product_obj = models.Products.objects.filter(id=id).first()
    pp_obj = models.ProductsPackages.objects.filter(product_id=id).all()
    pp2p_dict = {}
    for pp in pp_obj:
        pp2p_obj = models.ProductsPackages2P.objects.filter(pp2p=pp).all()
        pp2p_dict[pp.id] = pp2p_obj
    context = {
        'product_obj': product_obj,
        'pp_obj': pp_obj,
        'pp2p_dict': pp2p_dict,
        'title': '{}-下单'.format(product_obj),
        'user_info': user_dict,
        'default_city': default_city,
        'city_obj': city_obj,
    }
    return render(request, 'product/pp_buy.html', context)


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
                province_dict.append({'id': line.code, 'name': line.name, })
            elif line.r_code:
                city_dict.append({'id': line.code, 'name': line.name, 'pid': line.r_code})
            elif line.p_code:
                area_dict.append({'id': line.code, 'name': line.name, 'pid': line.p_code})

        result_dict['message'] = {'province': province_dict, 'city': city_dict, 'area': area_dict}
    # print(result_dict)
    return JsonResponse(result_dict)


from django import conf


def get_town(request, code):
    base_dir = conf.settings.BASE_DIR

    file_path = base_dir + r'\static\town\{}.json'.format(str(code))
    # print(file_path)
    # file_path =r'I:\django\sdy_new\static\town\440606.json'

    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read()
        # print(data)
    return HttpResponse(data)
