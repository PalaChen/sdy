# coding:utf-8
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from utils.menu import get_cate_list, user_info
from reposition import models, model_add
from django.db.models import Q
from reposition import models
from app.forms import account
import datetime
from django.utils import timezone
from app.views.product_method import *
from utils.login import wap_login_required
from utils.alipay import wap_alipay

title = {'city': '地区选择',
         'register': '注册',
         'login': '登陆',
         'mycenter': '个人中心',
         'findpass': '找回密码',
         'category': '分类',
         'commentlist': '评论页面',
         'serinfverify': '确认服务信息',
         'selectset': '选择套餐',
         'coupon': '优惠卷',
         'shopping': '购物车',
         'modeofpay': '选择支付方式',
         'orderlist': '订单列表',
         'orderProcess': '订单进展',
         }


def city(request):
    nid = request.GET.get('nid')
    city_obj = models.RegionalManagement.objects.filter(Q(r_code__isnull=False)).all()
    default_city = request.session.get('default_city')
    context = {
        'city_obj': city_obj,
        'default_city': default_city,
        'title': title['city'],
        'nid': nid,
    }
    return render(request, 'wap/city.html', context)


# 切换城市
def switch_city(request):
    result_dict = {'status': True, 'message': '', 'url': '', }
    if request.method == 'POST':
        nid = request.POST.get('nid')
        pid = request.POST.get('pid')
        city_obj = models.RegionalManagement.objects.filter(id=nid).first()
        if city_obj:
            area_obj = models.RegionalManagement.objects.filter(p_code=city_obj.code).first()
            request.session['default_city'] = {'city_id': city_obj.id, 'city': city_obj.name,
                                               'area_id': area_obj.id, 'city_code': city_obj.code}

            if pid:
                try:
                    # 获取当前地区的所对应的分类的产品
                    product_obj = models.Products.objects.filter(p_service_id=pid,
                                                                 area_id=area_obj.id).values('id').first()
                    if product_obj:
                        result_dict['url'] = 'product/{}.html'.format(product_obj['id'])
                        return JsonResponse(result_dict)
                except ValueError as e:
                    pass
            result_dict['url'] = '/wap/'
            return JsonResponse(result_dict)
        else:
            result_dict['message'] = '该城市暂不支持'
    else:
        result_dict['message'] = '非法请求'
    result_dict['status'] = False
    return JsonResponse(result_dict)


# 首页
def index(request):
    user_dict = user_info(request)
    default_city = request.session.get('default_city')
    context = {
        'default_city': default_city,
        'currentPage': 1,
    }
    return render(request, 'wap/index.html', context)


# 登陆
def login(request):
    if request.method == 'POST':
        result_dict = {'code': 1, 'msg': ''}
        form = account.LoginForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            phone = data.get('phone')
            password = data.get('password')
            user_obj = models.Users.objects.filter(phone=phone).values('id', 'name', 'password').first()
            if user_obj:
                # print(user_obj)
                # print(user_obj['password'])
                if user_obj['password'] == password:
                    request.session['user_info'] = {'phone': phone, 'id': user_obj['id'], 'name': user_obj['name']}
                    request.session['is_login'] = 'true'
                    return JsonResponse(result_dict)

                else:
                    result_dict['msg'] = '账号密码输入有误，请重新输入'
            else:
                result_dict['msg'] = '该手机号码暂未注册，请先注册'
        else:
            result_dict['msg'] = list(form.errors.values())[0][0]
        result_dict['code'] = 0
        return JsonResponse(result_dict)
    context = {'title': title['login']}
    return render(request, 'wap/login.html', context)


# 登出
def logout(request):
    del request.session['user_info']
    del request.session['is_login']
    return redirect('wap_mycenter')


# 注册
def register(request):
    if request.method == 'POST':
        result_dict = {'status': True, 'message': None}
        form_obj = account.WapRegisterForm(request.POST)
        if form_obj.is_valid():
            data = form_obj.cleaned_data
            verify_code = data.pop('verify_code')
            phone = data['phone']
            del data['password2']
            verify_info = models.MessagesVerifyCode.objects.filter(m_phone=phone, ) \
                .values_list('m_verifycode', 'm_send_date').order_by('-m_send_date').first()
            # 防止用户输入的手机号码和系统中发送短信手机号码不一致
            if verify_info:
                # 短信验证码时效性验证
                if (timezone.now() - verify_info[1]).seconds <= 1800:
                    # 短信验证码判断
                    if int(verify_code) == verify_info[0]:
                        res_obj = model_add.Add_info(models.Users, data)
                        if res_obj:
                            request.session['user_info'] = {'phone': res_obj.phone, 'id': res_obj.id,
                                                            'name': res_obj.name}
                            request.session['is_login'] = 'true'

                            return JsonResponse(result_dict)
                        else:
                            form_obj.errors['phone'] = ['手机号码已存在', ]
                    else:
                        result_dict['message'] = '短信验证码输入错误，请重新输入'
                else:
                    result_dict['message'] = '短信验证码超时，请重新获取'

            else:
                result_dict['message'] = '接受短信的手机号码和输入对的手机号码不一致',
        else:
            result_dict['message'] = list(form_obj.errors.values())[0][0]
        result_dict['status'] = False
        return JsonResponse(result_dict)
    context = {'title': title['register']}
    return render(request, 'wap/register.html', context)


# 个人中心
def mycenter(request):
    user_dict = user_info(request)
    if user_dict:
        if user_dict.get('id'):
            coupon_num = models.Coupon2User.objects.filter(user_id=user_dict['id']).count()
            shop_list = request.session.get('shop_list')
            if shop_list:
                user_dict['shop_number'] = len(shop_list['product'])
            else:
                user_dict['shop_number'] = 0
            user_dict['coupon_number'] = coupon_num

            context = {'title': title['mycenter'],
                       'user_dict': user_dict,
                       'currentPage': 4, }
            return render(request, 'wap/mycenter_islogin.html', context)
    context = {'title': title['mycenter'],
               'currentPage': 4}
    return render(request, 'wap/mycenter.html', context)


def question(request):
    """
    常见问题页面
    :param request:
    :return:
    """
    contxt = {'title': '常见问题'}
    return render(request, 'wap/question.html', contxt)


def aboutus(request):
    """
    关于我们页面
    :param request:
    :return:
    """
    contxt = {'title': '关于我们'}
    return render(request, 'wap/aboutus.html', contxt)


# 找回密码
def findpass(request):
    if request.method == 'POST':
        result_dict = {'status': True, 'message': None, }
        form = account.WapForgetPassForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data.pop('password2')
            verify_code = data.pop('verify_code')
            phone = data['phone']
            verify_info = models.MessagesVerifyCode.objects.filter(m_phone=phone, ) \
                .values_list('m_verifycode', 'm_send_date').order_by('-m_send_date').first()
            # 防止用户输入的手机号码和系统中发送短信手机号码不一致
            if verify_info:
                # 短信验证码时效性验证
                if (timezone.now() - verify_info[1]).seconds <= 1800:
                    # 短信验证码判断
                    if int(verify_code) == verify_info[0]:
                        models.Users.objects.filter(phone=phone).update(password=data['password'])
                        result_dict['url'] = '/wap/mycenter.html'
                        return JsonResponse(result_dict)
                    else:
                        result_dict['message'] = ['短信验证码输入错误，请重新输入', ]
                else:
                    result_dict['message'] = ['短信验证码超时，请重新获取', ]
            else:
                result_dict['message'] = ['接受短信的手机号码和输入对的手机号码不一致', ]

        else:
            result_dict['message'] = list(form.errors.values())[0][0]
        result_dict['status'] = False
        return JsonResponse(result_dict)
    context = {'title': title['findpass']}
    return render(request, 'wap/findpass.html', context)


# 评论列表
def commentlist(request):
    return render(request, 'wap/commentlist.html')


# 产品详情页
def productinfo(request, nid):
    default_city = request.session.get('default_city')
    product_obj = models.Products.objects.filter(id=nid, area_id=default_city['area_id']).first()
    if product_obj:
        service = get_object_or_404(models.ProductService, id=product_obj.p_service_id)
        service_obj = models.ProductService.objects.filter(root_id=service.root_id).all()
    else:
        return redirect('wap_index')
    # 城市列表
    city_obj = models.RegionalManagement.objects.filter(Q(r_code__isnull=False)).all()
    ared_obj = models.RegionalManagement.objects.filter(p_code=default_city['city_code']).all()
    context = {
        'product_obj': product_obj,
        'service_obj': service_obj,
        'default_city': default_city,
        'city_obj': city_obj,
        'ared_obj': ared_obj,
        'title': product_obj.p_name,
    }
    return render(request, 'wap/productinfo.html', context)


# 通过业务查找产品
def getProduct(request, nid):
    # result_dict = {'status': True, 'message': None, 'url': None}
    if request.method == 'GET':
        default_city = request.session['default_city']
        product_obj = models.Products.objects.filter(p_service_id=nid,
                                                     area_id=default_city['area_id']).values('id').first()

        if product_obj:
            return redirect('wap_productinfo', product_obj['id'])

    return redirect('wap_index')
    # else:
    #     result_dict['message'] = '非法请求'
    # result_dict['status'] = False
    # return JsonResponse(result_dict)


# 获取产品
def switch_product(request):
    result_dict = {'status': True, 'message': '', 'url': '', }
    if request.method == 'POST':
        area_code = request.POST.get('code')
        nid = request.POST.get('nid')

        area_obj = models.RegionalManagement.objects.filter(code=area_code).first()
        if area_obj:
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
                result_dict['url'] = 'product/{}.html'.format(product_obj['id'])
                return JsonResponse(result_dict)
            else:
                result_dict['message'] = '该地区暂无该产品'
        else:
            result_dict['message'] = '区域数据有误'
    else:
        result_dict['message'] = '非法请求'
    result_dict['status'] = False
    return JsonResponse(result_dict)


# 选择页
def selectset(request, product_id):
    packages_obj = models.Product2Package.objects.filter(product_id=product_id).all()
    if packages_obj:
        pacakage_list = []
        for package_obj in packages_obj:
            package2products_obj = models.Package2Product.objects.filter(package=package_obj.package).all()
            product_list = []
            for package2product in package2products_obj:
                product_dict = {'p_name': package2product.product.p_name,
                                'p_price': package2product.product.p_price}
                product_list.append(product_dict)
            # 如果套餐中已经包含商品，则添加入购物车
            pacakage_dict = {
                'name': package_obj.package.name,
                'info': {'id': package_obj.package.id,
                         'description': package_obj.package.dscription,
                         'cprice': package_obj.package.cprice,
                         'original_price': package_obj.package.original_price,
                         "product": product_list}}
            pacakage_list.append(pacakage_dict)
        context = {
            'title': title['selectset'],
            'pacakage_list': pacakage_list,
            'product_id': product_id,
        }
        return render(request, 'wap/selectset.html', context)
    return redirect('wap_serinfverify', product_id)


# 购买套餐页
def buy_pacakage(request):
    result_dict = {'status': True, 'message': '', 'url': '', }
    if request.method == 'POST':
        shop_list = request.session.get('shop_list')
        if not shop_list:
            shop_list = {'info': {}, 'coupon': {'price': 0, 'coupon_id': []}, 'product': []}
        p_id = request.POST.get('pid')
        pp_id = request.POST.get('ppid')

        if p_id and pp_id:
            package_obj = models.Package.objects.filter(id=pp_id).first()
            if not package_obj:
                package_obj = None
            product_dict = models.Products.objects.filter(id=p_id).values('p_name', 'p_business_id', 'p_price',
                                                                          'p_category__name', 'area__name',
                                                                          'city__name').first()
            if product_dict:
                product_dict.update({'product_id': p_id})

            shop_list = shop_list_append(product_dict, shop_list, package_obj)
            request.session['shop_list'] = shop_list
            result_dict['url'] = '/wap/shopping.html'
            return JsonResponse(result_dict)
        else:
            result_dict['message'] = '请求错误，请重新输入'
    else:
        result_dict['message'] = '非法请求'
    result_dict['status'] = False
    return JsonResponse(result_dict)


# 产品套餐页
def buy_product(request):
    """
    nid =[{"nid":"11","price":"111.1"},{"nid":"11","price":"111.1"},{"nid":"13","price":"119"}]
    :param request:
    :return:
    """

    result_dict = {'status': True, 'message': '', 'url': '', }
    if request.method == 'POST':
        # print('request.POST', request.POST)
        data_list = request.POST.getlist('nid')
        # print('data_list', data_list)
        shop_list = request.session.get('shop_list')
        if not shop_list:
            shop_list = {'info': {}, 'coupon': {'price': 0, 'coupon_id': []}, 'product': []}
        # print('data_list',type(data_list[0]))
        for data in eval(data_list[0]):
            # print('data', type(data), data)
            p_id = data['nid']
            # 产品
            if p_id:
                product_dict = models.Products.objects.filter(id=p_id).values('p_name', 'p_business_id', 'p_price',
                                                                              'p_category__name', 'area__name',
                                                                              'city__name').first()
            else:
                product_dict = {}

            if product_dict:
                product_dict.update({'product_id': p_id})
            shop_list = shop_list_append(product_dict, shop_list)
        request.session['shop_list'] = shop_list
        result_dict['status'] = 200
        result_dict['url'] = '/wap/shopping.html'
        return JsonResponse(result_dict)
    else:
        result_dict['message'] = '非法请求'
    result_dict['status'] = False
    return JsonResponse(result_dict)


#
def serinfverify(request, product_id):
    product_obj = models.Products.objects.filter(id=product_id).first()
    pp_obj = models.ProductsPackages.objects.filter(product_id=product_id).all()
    pp2p_dict = {}
    for pp in pp_obj:
        pp2p_obj = models.ProductsPackages2P.objects.filter(pp2p=pp).all()
        pp2p_dict[pp.id] = pp2p_obj
    context = {
        'product_obj': product_obj,
        'pp_obj': pp_obj,
        'pp2p_dict': pp2p_dict,
        'title': title['serinfverify'],
    }
    return render(request, 'wap/serinfverify.html', context)


# 购物车
@wap_login_required
def shopping(request):
    user_info = request.session.get('user_info')
    if user_info:
        shop_list = request.session.get('shop_list')
        if shop_list:
            shop_number = len(shop_list['product'])
        else:
            shop_number = 0
        context = {
            'shop_list': shop_list,
            'shop_number': shop_number,
            'title': title['shopping'],
        }

    else:
        return redirect('wap_login')
    return render(request, 'wap/shopping.html', context)


@wap_login_required
def numOfProduct(request):
    result_dict = {'status': True, 'message': '', 'url': '', }
    if request.method == 'POST':

        data = request.POST
        shop_list = request.session['shop_list']

        if data.get('number'):
            commodity_type = 'p_id'
            if int(data.get('type')) == 1:
                commodity_type = 'pp_id'

            for n, key in enumerate(shop_list['product']):
                if str(key.get(commodity_type)) == str(data['nid']):
                    shop_list['product'][n]['basic']['info']['number'] = data['number']
            # print(shop_list[n]['basic']['info']['number'], '--------', data['number'])
            # print(shop_list)
            request.session['shop_list'] = shop_list
            # print(shop_list)
            return JsonResponse(result_dict)
    else:
        result_dict['message'] = '非法请求'
    result_dict['status'] = False
    return JsonResponse(result_dict)


@wap_login_required
def delProduct(request):
    pid = None
    key = None
    result_dict = {'status': True, 'message': '', 'url': '', }
    if request.method == 'GET':
        try:
            shop_type = int(request.GET.get('type'))
            if shop_type == 0:
                key = 'p_id'
                pid = request.GET.get('pid')
            else:
                key = 'pp_id'
                pid = request.GET.get('ppid')
        except ValueError as e:
            result_dict['message'] = '非法请求'
            result_dict['status'] = False

        shop_list = request.session.get('shop_list')
        for index, shop in enumerate(shop_list['product']):
            if key in shop.keys() and str(shop[key]) == str(pid):
                del shop_list['product'][index]
        request.session['shop_list'] = shop_list
        return JsonResponse(result_dict)
    else:
        result_dict['message'] = '非法请求'
    result_dict['status'] = False
    return JsonResponse(result_dict)


@wap_login_required
def buy(request):
    result_dict = {'status': True, 'message': '', 'url': '', }
    user_dict = request.session.get('user_info')
    shop_list = request.session.get('shop_list')
    # print('shop_list-->',shop_list)
    import time, random
    order_code = time.strftime('%Y%m%d%H%M%S', time.localtime()) + str(random.randint(11, 99))
    if shop_list.get('product'):
        # 创建数据
        # print(shop_list)
        for item in shop_list.get('product'):
            # shop_list.get('product')表的样子
            """
            [{'p_id': 14, 'basic': {'type': '0', 'info': {
                'pid': 14, 'number': 1, 'detail': {
                    'p_business': 1, 'area__name': '顺德区', 'city__name': '佛山市', 'p_category__name': '有限公司注册',
                    'p_name': '111', 'p_price': 111.1}}}}

             {'pp_id': 1, 'basic': {'type' = 1, {'info': {'ppid': 11,
                                                          'name': 123123
                                                          'number': 1,
                                                          'cprice': 222,
                                                          'detail': [{'p_business': 1, 'area__name': '顺德区',
                                                                      'city__name': '佛山市', 'p_category__name': '有限公司注册',
                                                                      'p_name': '111', 'p_price': 111.1}, ]}}}}
            ]
            """
            # print('item-->', item)
            for line in item['basic']['info']['detail']:
                number = item['basic']['info']['number']
                cprice = line['p_price']
                total_price = float(number) * float(cprice)

                data = {}
                data['product_id'] = line['product_id']
                data['product_name'] = line['p_name']
                data['cprice'] = line['p_price']
                data['number'] = item['basic']['info']['number']
                data['total_price'] = total_price
                data['category'] = line['p_category__name']
                data['p_business_id'] = line['p_business_id']
                data['city'] = line['city__name']
                data['area'] = line['area__name']
                data['phone'] = user_dict['phone']
                data['name'] = user_dict['name']
                data['user_id'] = user_dict['id']
                data['order_code'] = order_code
                models.Orders.objects.create(**data)
    else:
        result_dict['status'] = False
        result_dict['url'] = '/cart.html'
        return JsonResponse(result_dict)
    # order_obj = models.Orders.objects.filter(order_code=order_code).values('order_code', 'product_name', 'number').all()
    pay_data = {}
    pay_data['order_code'] = order_code
    pay_data['user_id'] = user_dict['id']
    pay_data['total_price'] = request.POST.get('total_price')
    pay_data['coupon_price'] = request.POST.get('coupon_price')
    pay_data['pay_price'] = request.POST.get('pay_price')
    pay_obj = models.OrderPayment.objects.create(**pay_data)
    request.session['shop_list'] = None
    result_dict['url'] = '/wap/modeofpay/{}.html'.format(pay_obj.id)
    return JsonResponse(result_dict)


# 优惠卷
def coupon(request):
    return render(request, 'wap/coupon.html')


def modeofpay(request, nid):
    """
    支付页面
    :param request:
    :param nid:
    :return:
    """
    pay_obj = models.OrderPayment.objects.filter(id=nid).first()
    if pay_obj:
        if pay_obj.status == 1:
            return redirect('wap_orderlist')

        order_obj = models.Orders.objects.filter(order_code=pay_obj.order_code) \
            .values('order_code', 'product_name', 'number', 'city', 'area').all()
        context = {
            'order_obj': order_obj,
            'title': title['modeofpay'],
            'pay_obj': pay_obj,
        }
        return render(request, 'wap/modeofpay.html', context)
    return redirect('wap_index')


def order_topay(request, nid):
    """
    订单页面跳转到支付页面
    :param request:
    :param nid:
    :return:
    """
    if request.method == 'GET':
        phone = request.session.get('user_info')['phone']
        order_obj = models.Orders.objects.filter(id=nid, phone=phone).all()
        if order_obj:
            pay_dict = models.OrderPayment.objects.filter(order_code=list(order_obj)[0].order_code).first()
            if pay_dict:
                if pay_dict.status == 1:
                    for line in order_obj:
                        line.order_state = 1
                        line.save()
                else:
                    return redirect('wap_modeofpay', pay_dict.id)
    return redirect('wap_orderlist')


def payment_method(request):
    result_dict = {'status': True, 'message': '', 'url': '', }
    if request.method == 'POST':
        pay_id = request.POST.get('nid')
        payment_method = request.POST.get('bankid')

        pay_obj = models.OrderPayment.objects.filter(id=pay_id).first()
        pay_obj.payment = payment_method
        pay_obj.save()

        models.Orders.objects.filter()

        if payment_method == '0':
            tn = pay_obj.order_code,  # 订单编号
            subject = '盛德业订单支付',  # 订单名称
            body = '盛德业订单支付',  # 订单描述
            tf = pay_obj.pay_price
            url = wap_alipay.create_direct_pay_by_user(tn, subject, body, tf)
            result_dict['url'] = url
            return JsonResponse(result_dict)
    else:
        result_dict['message'] = '非法请求'
    result_dict['status'] = False
    return JsonResponse(result_dict)


def get_alipay_info(request):
    # print('--------->', request)
    data = {}
    # 订单号
    data['out_trade_no'] = request.get('out_trade_no')
    # 支付宝单号
    data['trade_no'] = request.get('trade_no')
    # 交易状态
    data['trade_status'] = request.get('trade_status')
    # 交易方式
    data['payment_type'] = request.get('payment_type')
    # 交易时间
    data['notify_time'] = request.get('notify_time')
    # 成功状态
    data['is_success'] = request.get('is_success')
    # 通知类型
    data['notify_type'] = request.get('notify_type')
    # 用户标识
    data['buyer_id'] = request.get('buyer_id')
    # 买家邮箱
    data['buyer_email'] = request.get('buyer_email')
    # 交易金额
    data['total_fee'] = request.get('total_fee')
    return data


def save_alipy_info(alipay_dict):
    # print('alipay_dict------->', alipay_dict)
    order_code = alipay_dict.get('out_trade_no')
    # print(order_code)

    OrderPaymen_obj = models.OrderPayment.objects.filter(order_code=order_code).first()

    if OrderPaymen_obj:
        paymengAlipy_obj = models.PaymengAlipy.objects.filter(pay_id=OrderPaymen_obj.id).first()
        # 防止移动端重复点击多次支付宝钱包支付，页面自动跳转
        if paymengAlipy_obj:
            return True

        OrderPaymen_obj.status = 1
        OrderPaymen_obj.payment = 0
        OrderPaymen_obj.ftime = datetime.datetime.now()
        OrderPaymen_obj.save()
        alipay_dict['pay_id'] = OrderPaymen_obj.id
        models.PaymengAlipy.objects.create(**alipay_dict)

    # 更改同一个订单号的所有订单的状态
    order_obj = models.Orders.objects.filter(order_code=order_code).all()
    if order_obj:
        for line in order_obj:
            line.order_state = 1
            line.save()
            order_serice_dict = {
                'order_id': line.id,
                'city': line.city,
                'area': line.area,

            }
            models.OrderSerice.objects.create(**order_serice_dict)

    return True


@csrf_exempt
def alipay_return_url(request):
    """支付宝接口同步请求"""
    if wap_alipay.notify_verify(request.GET):
        alipay_dict = get_alipay_info(request.GET)
        res = save_alipy_info(alipay_dict)
        if res:
            return redirect('wap_orderlist')

    return redirect('wap_index')


@csrf_exempt
def alipay_notify_url(request):
    if request.method == 'POST':
        if wap_alipay.notify_verify(request.POST):
            alipay_dict = get_alipay_info(request.GET)
            save_alipy_info(alipay_dict)
            return HttpResponse("success")
    return HttpResponse("fail")


@wap_login_required
def orderlist(request):
    user_dict = user_info(request)
    order_obj = models.Orders.objects.filter(phone=user_dict['phone'], order_state__in=[0, 1, 2, 4, 5]).order_by(
        '-ctime').all()
    # 1 未付款 2 办理中 3 待评价
    orderState_dict = {1: 0, 2: 0, 3: 0, 4: 0}
    order_dict = {}
    """
    order_dict
    [{'订单号':{'num':1,status:0;'product':[]}}}},{'订单号':{'num':1,status:0;'product':[]}}}},]
    """
    for order in order_obj:
        order_code = order.order_code

        if order_code in order_dict.keys():
            order_dict[order_code]['num'] += 1
            order_dict[order_code]['product'].append(order)
        else:
            order_dict.update({order_code: {'num': 1, 'status': order.order_state, 'product': []}})
            order_dict[order_code]['product'].append(order)
        # 统计未付款、已付款的数据量
        order_state = order.order_state
        if order_state == 0:
            orderState_dict[1] += 1
        elif order_state in [1, 2, 5]:
            orderState_dict[1] += 1
        elif order_state == 4:
            orderState_dict[2] += 1
    context = {
        'order_dict': order_dict,
        'title': title['orderlist'],
        'orderState_dict': orderState_dict,
        'currentPage': 3,
    }
    return render(request, 'wap/orderlist.html', context)


@wap_login_required
def cancelorders(request, nid):
    """
    取消订单
    :param request:
    :return:
    """
    order_obj = models.Orders.objects.filter(id=nid).first()
    if order_obj:
        models.OrderPayment.objects.filter(order_code=order_obj.order_code).update(status=3)
        models.Orders.objects.filter(order_code=order_obj.order_code).update(order_state=3)
    return redirect('wap_orderlist')


@wap_login_required
def orderRefund(request, nid):
    """
    申请退款
    :param request:
    :param nid:
    :return:
    """
    order_obj = models.Orders.objects.filter(id=nid).first()
    if order_obj:
        models.Orders.objects.filter(order_code=order_obj.order_code).update(order_state=5)
    return redirect('wap_orderlist')


@wap_login_required
def cancelRefund(request, nid):
    """
    取消退款
    :param request:
    :param nid:
    :return:
    """
    order_obj = models.Orders.objects.filter(id=nid).first()
    if order_obj:
        models.Orders.objects.filter(order_code=order_obj.order_code).update(order_state=2)
    return redirect('wap_orderlist')


@wap_login_required
def orderProcess(request, nid):
    order_obj = models.Process.objects.filter(order_id=nid).values('step_name', 'date').order_by('date')
    context = {'title': title['orderProcess'],
               'order_obj': order_obj, }
    return render(request, context)


def category(request):
    cate_list = get_cate_list()

    context = {'cate_list': cate_list,
               'title': title['category'],
               'currentPage': 2}
    return render(request, 'wap/category.html', context)


def p_category(request, nid):
    default_city = request.session['default_city']
    product_obj = models.Products.objects.filter(p_category_id=nid, area_id=default_city['area_id']).first()
    if product_obj:
        return redirect('wap_productinfo', product_obj.id)
    else:
        return redirect('wap_index')
