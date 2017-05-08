from django.shortcuts import render, redirect, HttpResponse
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
# @permission
def manage(request, *args, **kwargs):
    menu_string = kwargs.get('menu_string')
    common_info = {}
    common_info['menu_string'] = kwargs.get('menu_string')
    common_info['title'] = title_dict['manage']
    common_info['html_url'] = 'service/service_manage.html'
    common_info['employee_obj'] = models.Employees.objects.filter(status=0).values('id', 'name').all()
    return base.table_obj_list(request, 'reposition', 'orderserice', common_info)


@login_required
def assign_employee(request):
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
    process_obj = models.Process.objects.filter(order_id=id).values('process_name',
                                                                    'step_name',
                                                                    'employee_name',
                                                                    'date').order_by('date').all()
    result_dict['tbbody'] = list(process_obj)
    return JsonResponse(result_dict)


@login_required
# @permission
def order(request, *args, **kwargs):
    action_list = kwargs.get('action_list')
    menu_string = kwargs.get('menu_string')
    order_code_list = models.Orders.objects.values('ctime', 'order_code').distinct()
    order_obj = models.Orders.objects.all().order_by('-ctime')
    # models.Orders.objects.filter()
    return render(request, 'service/order.html', {'menu_string': menu_string,
                                                  'order_obj': order_obj,
                                                  'order_code_list': order_code_list,
                                                  'title': title_dict['order']})


@login_required
# @permission
def order_add(request, *args, **kwargs):
    menu_string = kwargs.get('menu_string')
    return render(request, 'service/order_add.html', {'menu_string': menu_string,
                                                      'title': title_dict['order_add']})


@login_required
# @permission
def payment(request, *args, **kwargs):
    common_info = {}
    common_info['menu_string'] = kwargs.get('menu_string')
    common_info['title'] = title_dict['payment']
    return base.table_obj_list(request, 'reposition', 'orderpayment', common_info)
