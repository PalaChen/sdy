# coding:utf-8
from django.shortcuts import render, redirect, HttpResponse
from django.db import connection
from django.http import JsonResponse
from backend.forms.service import AssignEmployeeForm
from reposition import models
from utils.login_admin import login_required, permission
from cxmadmin import base
from datetime import datetime

result_dict = {'status': 200, 'message': None, 'data': None}
title_dict = {'manage': '分配管理', 'order': '订单管理', 'order_add': '订单添加',
              'payment': '支付管理'}


# 分配管理
@login_required
@permission
def manage(request, *args, **kwargs):
    common_info = {}
    common_info['menu_string'] = kwargs.get('menu_string')
    common_info['title'] = title_dict['manage']
    common_info['html_url'] = 'service/service_manage.html'
    common_info['employee_obj'] = models.Employees.objects.filter(status=0).values('id', 'name').all()
    return base.table_obj_list(request, 'reposition', 'orderserice', common_info)


@login_required
def assign_employee(request):
    result_dict = {'status': 200, 'message': None, 'data': None}
    form_obj = AssignEmployeeForm(request.POST)
    if form_obj.is_valid():
        form_obj.save()
        models.OrderSerice.objects.filter(id=request.POST.get('order_serice')).update(allocation_status=1,
                                                                                      status=1,
                                                                                      start_time=datetime.now())

        models.Orders.objects.filter(id=request.POST.get('order')).update(order_state=2)
        result_dict['message'] = '分配任务成功'
    else:
        result_dict['status'] = 800
        result_dict['message'] = list(form_obj.errors.values())[0][0]
    return JsonResponse(result_dict)


# @login_required
def order_business(request, id, *args, **kwargs):
    result_dict = {'status': 200, 'message': None, 'data': None}
    process_obj = models.Process.objects.filter(order_id=id).values('process_name',
                                                                    'step_name',
                                                                    'employee_name',
                                                                    'date').order_by('date').all()
    result_dict['tbbody'] = list(process_obj)
    return JsonResponse(result_dict)


def dictfetchall(cursor):
    """将游标返回的结果保存到一个字典对象中"""
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]


@login_required
@permission
def order(request, *args, **kwargs):
    action_list = kwargs.get('action_list')
    menu_string = kwargs.get('menu_string')
    order_code_list = models.Orders.objects.values('ctime', 'order_code').distinct()
    from django.db import DefaultConnectionProxy
    cursor = connection.cursor()
    cursor.execute("SELECT B.*,A.payment FROM orders_payment AS A LEFT JOIN orders AS B ON A.order_code=B.order_code")
    order_obj = dictfetchall(cursor)
    models.Orders.objects.filter()
    status_dict = {0: '待付款', 1: '待服务', 2: '服务中', 3: '服务完成', 4: '退款中', 5: '退款完成', 6: '交易关闭'}
    payment_dict = {0: '支付宝', 1: '微信', 2: '线下支付', 3: '网银支付'}
    order_status_dict = {'status': status_dict, 'payment': payment_dict}
    return render(request, 'service/order.html', {'menu_string': menu_string,
                                                  'order_obj': order_obj,
                                                  'order_code_list': order_code_list,
                                                  'order_status_dict': order_status_dict,
                                                  'title': title_dict['order']})


@login_required
def pay_state(request):
    result_dict = {'status': 200, 'message': '订单状态修改成功', 'data': None}
    code = request.POST.get('code')
    status = request.POST.get('status')
    payment = request.POST.get('payment')

    models.OrderPayment.objects.filter(order_code=code).update(status=status, payment=payment)
    order_obj = models.Orders.objects.filter(order_code=code).all()
    if order_obj:
        for line in order_obj:
            line.order_state = 1
            line.save()
            order_serice_dict = {
                'order_id': line.id,
                'city': line.city,
                'area': line.area,

            }
            try:
                models.OrderSerice.objects.create(**order_serice_dict)
            except Exception as e:
                pass
        return JsonResponse(result_dict)
    else:
        result_dict['status'] = 404
        result_dict['message'] = '非法操作'
    return JsonResponse(result_dict)


# @login_required
# # @permission
# def order_add(request, *args, **kwargs):
#     menu_string = kwargs.get('menu_string')
#     common_info = {}
#     common_info['title'] = title_dict['order_add']
#     common_info['redirect_url'] = 'service_order'
#     common_info['return_link'] = 'service_order'
#     common_info['menu_string'] = kwargs.get('menu_string')
#     return base.table_obj_add(request, 'reposition', 'clientinfo', common_info)


@login_required
@permission
def payment(request, *args, **kwargs):
    common_info = {}
    common_info['menu_string'] = kwargs.get('menu_string')
    common_info['title'] = title_dict['payment']
    # common_info['html_url'] = 'service/payment.html'
    return base.table_obj_list(request, 'reposition', 'orderpayment', common_info)
