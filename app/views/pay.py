# coding:utf-8
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from reposition import models
from utils.login import login_required
from utils.alipay import alipay
import datetime
import time
import random
from django.db.models import Q
from django.db import connection, connections

from utils.menu import user_info

# 方法
from . import product_method

title_dict = {'cart': '购物车', 'pay': '支付'}
result_dict = {'status': 200, 'message': None, 'data': None}
status = {
    200: '正常',
    501: '信息不存在',
    801: '用户不存在',
    802: '支付失败'

}
city_obj = models.RegionalManagement.objects.filter(Q(r_code__isnull=False)).all()


@login_required
def cart(request):
    """
    购物车
    :param request:
    :return:
    """
    if request.method == 'POST':
        result_dict = {'status': 200, 'message': None, 'data': None}
        shop_list = product_method.productPackage_info(request)
        if shop_list:
            request.session['shop_list'] = shop_list
            result_dict['status'] = 200
            result_dict['url'] = '/cart.html'
        # product_method.shop_list_append(package_obj, product_dict, shop_list)
        else:
            result_dict['status'] = False
            result_dict['message'] = '请求非法数据'
        return JsonResponse(result_dict)

    else:
        default_city = request.session.get('default_city')
        user_dict = user_info(request)
        is_login = request.session.get('is_login')
        shop_list = product_method.cart_info(request)

        # print(user_info['id'])
        coupon_obj = models.Coupon2User.objects.filter(user_id=user_dict['id'])
        # print(shop_list)

        request.session['shop_list'] = shop_list
        if shop_list:
            user_dict['shop_number'] = len(shop_list['product'])
        else:
            user_dict['shop_number'] = 0
        # print('user_info.shop_number-->', user_info['shop_number'])
        context = {'shop_list': shop_list,
                   'user_info': user_dict,
                   'is_login': is_login,
                   'default_city': default_city,
                   'coupon_obj': coupon_obj,
                   'city_obj': city_obj,
                   'title': title_dict['cart']}
        return render(request, 'shop/index.html', context)


@login_required
def cart_number(request):
    data = request.POST
    result_dict = {'status': 200, 'message': None, 'data': None}
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


@login_required
def cart_del(request, ):
    result_dict = {'status': 200, 'message': None, 'data': None}
    pid = None
    key = None
    # print(request.GET)
    try:
        shop_type = int(request.GET.get('type'))
        if shop_type == 0:
            key = 'p_id'
            pid = request.GET.get('pid')
        else:
            key = 'pp_id'
            pid = request.GET.get('ppid')
    except ValueError as e:
        result_dict['status'] = 400
        return JsonResponse(result_dict)

    shop_list = request.session.get('shop_list')
    for index, shop in enumerate(shop_list['product']):
        if key in shop.keys() and str(shop[key]) == str(pid):
            del shop_list['product'][index]
    request.session['shop_list'] = shop_list

    return JsonResponse(result_dict)


@login_required
def coupon_add(request):
    coupon_id = request.POST.get('nid')
    price = request.POST.get('price')
    result_dict = {'status': 200, 'message': None, 'data': None}
    if coupon_id and coupon_id.isdigit() and price.isdigit():
        shop_list = request.session['shop_list']
        if int(coupon_id) not in shop_list['coupon']['coupon_id']:
            shop_list['coupon']['coupon_id'].append(int(coupon_id))
            shop_list['coupon']['price'] += int(price)
            request.session['shop_list'] = shop_list

    return JsonResponse(result_dict)


@login_required
def coupon_del(request):
    coupon_id = request.POST.get('nid')
    price = request.POST.get('price')
    result_dict = {'status': 200, 'message': None, 'data': None}
    if coupon_id and coupon_id.isdigit() and price.isdigit():
        shop_list = request.session['shop_list']
        if int(coupon_id) in shop_list['coupon']['coupon_id']:
            shop_list['coupon']['coupon_id'].remove(int(coupon_id))
            shop_list['coupon']['price'] -= int(price)
            request.session['shop_list'] = shop_list
    return JsonResponse(result_dict)


@login_required
# 　生成订单信息
def buy_info(request):
    user_dict = request.session.get('user_info')
    shop_list = request.session.get('shop_list')
    result_dict = {'status': 200, 'message': None, 'data': None}
    order_code = time.strftime('%Y%m%d%H%M%S', time.localtime()) + str(random.randint(11, 99))
    if shop_list.get('product'):
        # 创建数据
        for item in shop_list.get('product'):
            # shop_list表的样子
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
            # print(item)
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
        result_dict['status'] = 501
        result_dict['url'] = '/cart.html'
        return JsonResponse(result_dict)
    order_obj = models.Orders.objects.filter(order_code=order_code).values('order_code', 'product_name', 'number').all()
    pay_data = {}
    pay_data['order_code'] = order_code
    pay_data['user_id'] = user_dict['id']
    pay_data['total_price'] = request.POST.get('total_price')
    pay_data['coupon_price'] = request.POST.get('coupon_price')
    pay_data['pay_price'] = request.POST.get('pay_price')
    pay_obj = models.OrderPayment.objects.create(**pay_data)
    request.session['shop_list'] = None
    result_dict['url'] = '/pay/{}.html'.format(pay_obj.id)
    return JsonResponse(result_dict)


# 支付页面
def pay(request, id):
    default_city = request.session.get('default_city')

    user_dict = user_info(request)
    is_login = request.session.get('is_login')
    pay_obj = models.OrderPayment.objects.filter(id=id).first()
    if pay_obj:
        if pay_obj.status == 1:
            return redirect('user_order')

        order_obj = models.Orders.objects.filter(order_code=pay_obj.order_code) \
            .values('order_code', 'product_name', 'number', 'city', 'area').all()
        return render(request, 'shop/pay.html', {'order_obj': order_obj,
                                                 'is_login': is_login,
                                                 'pay_obj': pay_obj,
                                                 'user_info': user_dict,
                                                 'default_city': default_city,
                                                 'title': title_dict['pay']})
    return redirect('web_index')


def weixin(request, id):
    result_dict = {'status': 200, 'message': None, 'data': None}
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    pay_obj = models.OrderPayment.objects.filter(id=id).first()
    if pay_obj:
        if pay_obj.status == 1:
            result_dict['status'] = 301
            result_dict['url'] = '/user/order.html'
        else:
            from utils.wechatpay.wechatpay import WeChatPay
            wp = WeChatPay()
            price = int(pay_obj.pay_price * 100)
            res = wp.createPayment(ip, price, pay_obj.order_code)
            url = res.get('code_url')
            if url:
                result_dict['url'] = url
            else:
                result_dict['status'] = 201
                result_dict['message'] = '服务器请求出错，请重新购买'

    else:
        result_dict['status'] = 201
        result_dict['message'] = '非法请求'
    return JsonResponse(result_dict)


# 支付成功判断
def pay_judgment(request, nid):
    result_dict = {'status': 200, 'message': None, 'data': None}
    if request.method == 'GET':
        pay_obj = models.OrderPayment.objects.filter(id=nid).values('status').first()
        if pay_obj['status'] == 1:
            result_dict['status'] = True
            result_dict['url'] = '/user/order.html'
            return JsonResponse(result_dict)

        else:
            result_dict['status'] = False
            result_dict['url'] = '/pay/pay_fail.html?pid={}'.format(nid)
            return JsonResponse(result_dict)
    else:
        result_dict['status'] = False
        result_dict['message'] = '非法请求'
    return JsonResponse(result_dict)


# 支付失败
def pay_fail(request):
    nid = request.GET.get('pid')
    return render(request, 'shop/pay_fail.html', {'nid': nid})


# 选择付款方式
def payment_method(request):
    if request.method == 'POST':
        pay_id = request.POST.get('id')
        payment_method = request.POST.get('bankid')

        pay_obj = models.OrderPayment.objects.filter(id=pay_id).first()
        pay_obj.payment = payment_method
        pay_obj.save()

        models.Orders.objects.filter()

        if payment_method == '0':
            tn = pay_obj.order_code,  # 订单编号
            subject = '盛德业订单支付',  # 订单名称
            body = '盛德业订单支付',  # 订单描述
            bank = 'alipay',  # 扩展参数
            tf = pay_obj.pay_price
            url = alipay.create_direct_pay_by_user(tn, subject, body, bank, tf)
        return HttpResponseRedirect(url)


# alipay异步通知
@csrf_exempt
def alipay_notify_url(request):
    if request.method == 'POST':
        if alipay.notify_verify(request.POST):
            alipay_dict = get_alipay_info(request.GET)
            save_alipy_info(alipay_dict)
            return HttpResponse("success")
    return HttpResponse("fail")


# 微信异步通知
@csrf_exempt
def wxpay_ruturn_url(request):
    data_xml = request.body
    import xml.etree.ElementTree as ET
    data_dict = dict((child.tag, child.text) for child in ET.fromstring(data_xml))
    from utils.wechatpay.wechatpay import appid, mch_id
    if appid == data_dict.get('appid') and mch_id == data_dict.get('mch_id'):
        data_dict.pop('nonce_str')
        wechat_exit = models.PaymentWechat.objects.filter(**data_dict).first()
        if not wechat_exit:
            models.PaymentWechat.objects.create(**data_dict)

    return HttpResponse('OK')


# 同步通知
def alipay_return_url(request):
    if alipay.notify_verify(request.GET):
        alipay_dict = get_alipay_info(request.GET)
        res = save_alipy_info(alipay_dict)
        if res:
            return redirect('/user/order.html')

    return redirect("/")


# 外部跳转回来的链接session可能丢失，无法再进入系统。
# 客户可能通过xxx.com操作，但是支付宝只能返回www.xxx.com，域名不同，session丢失。
def pay_verify(request, cbid):
    # try:
    #     cb=cBill.objects.get(id=cbid)
    #     #如果订单时间距现在超过1天，跳转到错误页面！
    #     #避免网站信息流失
    #
    #     return render_to_response('public_verify.html',{'cb':cb},RequestContext(request))
    # except ObjectDoesNotExist:
    return HttpResponseRedirect("/err/no_object")


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
