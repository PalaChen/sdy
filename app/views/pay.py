from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from reposition import models
from utils.login import login_required
from utils.alipay import alipay
import datetime
import time
import random

title_dict = {'cart': '购物车', 'pay': '支付'}
result_dict = {'status': 200, 'message': None, 'data': None}
status = {
    200: '正常',
    501: '信息不存在',
    801: '用户不存在',
    802: '支付失败'

}


@login_required
def cart(request):
    default_city = request.session.get('default_city')
    user_info = request.session.get('user_info')
    id = request.GET.get('pid')
    is_login = request.session.get('is_login')
    product_dict = models.Products.objects.filter(id=id).values('p_name', 'p_business', 'p_price',
                                                                'p_category__name', 'area__name', 'city__name').first()
    # print('product_dict--->', product_dict)
    try:
        shop_list = request.session['shop_list']
    except KeyError:
        shop_list = {}

    if product_dict:
        try:
            if id in shop_list.keys():
                pass
            else:
                shop_list.update({id: {'info': product_dict, 'number': 1}})
        except AttributeError:
            # 对象不是一个not JSON serializable,
            shop_list = {id: {'info': product_dict, 'number': 1}}

    request.session['shop_list'] = shop_list

    return render(request, 'shop/index.html', {'shop_list': shop_list,
                                               'user_info': user_info,
                                               'is_login': is_login,
                                               'default_city':default_city,
                                               'title': title_dict['cart']})


@login_required
def cart_number(request):
    data = request.POST
    shop_list = request.session['shop_list']
    if data.get('number'):
        shop_list[data['product_id']]['number'] = data['number']

    print(shop_list)
    request.session['shop_list'] = shop_list
    return JsonResponse(result_dict)


@login_required
def cart_del(request, id):
    shop_list = request.session.get('shop_list')
    shop_list.pop(id)
    request.session['shop_list'] = shop_list
    return JsonResponse(result_dict)


# @login_required
# 　生成订单信息
def buy_info(request):
    user_info = request.session.get('user_info')
    shop_list = request.session.get('shop_list')
    order_code = time.strftime('%Y%m%d%H%M%S', time.localtime()) + str(random.randint(00, 99))
    if shop_list:
        for shop_key, shop_value in shop_list.items():
            # {'13': {'number': '2', 'info': {'p_price': 111.0, 'city__name': '佛山市', 'p_business': 1, 'p_name': '合伙企业注册', 'p_category__name': '合伙企业注册', 'area__name': '顺德区'}},}
            # v ={'info': {'p_name': '有限公司注册', 'number': '4', 'p_price': 11.0}}
            if shop_key == 'price':
                pass
            else:
                data = {}
                data['product_id'] = shop_key
                data['product_name'] = shop_value['info']['p_name']
                data['cprice'] = shop_value['info']['p_price']
                data['total_price'] = shop_value['info']['p_price']
                data['category'] = shop_value['info']['p_category__name']
                data['p_business_id'] = shop_value['info']['p_business']
                data['city'] = shop_value['info']['city__name']
                data['area'] = shop_value['info']['area__name']
                data['phone'] = user_info['phone']
                data['name'] = user_info['name']
                data['user_id'] = user_info['id']
                data['order_code'] = order_code

                for i in range(0, int(shop_value['number'])):
                    models.Orders.objects.create(**data)
    else:
        result_dict['status'] = 501
        result_dict['url'] = '/cart.html'
        return JsonResponse(result_dict)
    order_obj = models.Orders.objects.filter(order_code=order_code).values('order_code', 'product_name', 'number').all()
    pay_data = {}
    pay_data['order_code'] = order_code
    pay_data['user_id'] = user_info['id']
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
    user_info = request.session.get('user_info')
    is_login = request.session.get('is_login')
    pay_obj = models.OrderPayment.objects.filter(id=id).first()
    if pay_obj:
        if pay_obj.status == 1:
            return redirect('user_order')

        order_obj = models.Orders.objects.filter(order_code=pay_obj.order_code) \
            .values('order_code',
                    'product_name',
                    'number').all()
        return render(request, 'shop/pay.html', {'order_obj': order_obj,
                                                 'is_login': is_login,
                                                 'pay_obj': pay_obj,
                                                 'user_info': user_info,
                                                 'default_city':default_city,
                                                 'title': title_dict['pay']})
    return redirect('web_index')


# 支付成功判断
def pay_judgment(request, nid):
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
    print('--------->', request)
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
    print('alipay_dict------->', alipay_dict)
    order_code = alipay_dict.get('out_trade_no')
    print(order_code)

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
