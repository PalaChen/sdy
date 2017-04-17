from django.shortcuts import render, redirect
from django.http import JsonResponse
from reposition import models
from utils.login import login_required

import time
import random

title_dict = {'index': '购物车', 'pay': '支付'}
result_dict = {'status': 200, 'message': None, 'data': None}
status = {
    200: '正常',
    801: '用户不存在',
}


@login_required
def cart(request):
    id = request.GET.get('pid')
    product_dict = models.Products.objects.filter(id=id).values('p_name', 'p_price', ).first()
    shop_list = request.session.get('shop_list')

    if shop_list:
        if not id:
            pass
        elif id in shop_list.keys():
            pass
        else:
            shop_list.update({id: {'name': product_dict, 'number': 1}})
            request.session['shop_list'] = shop_list

    else:
        shop_list = {id: {'name': product_dict, 'number': 1},}
        request.session['shop_list'] = shop_list
    print(shop_list)
    return render(request, 'shop/index.html', {'shop_list': shop_list,
                                               'title': title_dict['index']})


@login_required
def cart_number(request):
    data = request.POST
    print(data)
    shop_list = request.session['shop_list']
    # request.session['shop_list'].update({'price': data['price']})
    if data.get('number'):
        shop_list[data['product_id']]['number'] = data['number']
    shop_list.update({'price': data['price']})
    request.session['shop_list'] = shop_list
    print(shop_list)

    return JsonResponse(result_dict)


@login_required
def cart_del(request, id):
    shop_list = request.session.get('shop_list')
    shop_list.pop(id)
    request.session['shop_list'] = shop_list
    return JsonResponse(result_dict)


@login_required
def pay(request):
    user_info = request.session.get('user_info')
    shop_list = request.session.get('shop_list')
    order_code = time.strftime('%Y%m%d%H%M%S', time.localtime()) + str(random.randint(00, 99))
    for k, v in shop_list.items():
        data = {}
        data['product_id'] = k
        data['product_name'] = v['name']['p_name']
        data['cprice'] = v['name']['p_price']
        data['phone'] = user_info['phone']
        data['number'] = v['number']
        data['name'] = user_info['name']
        data['user_id'] = user_info['id']
        data['order_code'] = order_code
        models.Orders.objects.create(**data)
    order_obj = models.Orders.objects.filter(order_code=order_code).values('order_code', 'product_name', 'number').all()
    pay_data = {}
    pay_data['order_code'] = order_code
    pay_data['user_id'] = user_info['id']
    pay_data['price'] = shop_list['price']
    models.OrderPayment.objects.create(**pay_data)

    return render(request, 'shop/pay.html', {'order_obj': order_obj,
                                             'order_code': order_code,
                                             'title': title_dict['pay']})
