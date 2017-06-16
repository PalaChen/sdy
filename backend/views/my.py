from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from reposition import models
from backend.forms.my import OrderBusinessAddForm
from utils.login_admin import permission, login_required
from cxmadmin import base
from datetime import datetime
from utils.sms_message import process_message_send

result_dict = {'status': True, 'message': None, 'data': None}
title_dict = {'task': '我的任务', 'client': '我的客户',
              'client_add': '客户添加',
              'client_edit': '客户修改',}


@login_required
@permission
def task(request, *args, **kwargs):
    common_info = {}
    filter_dict = {
        'employee_id': request.session.get('user_info')['employee_id'],
        'status': 0,
    }
    # models.ProcessStep.objects.filter(p_name=)
    employee_obj = models.Employees.objects.filter(status=0).all()
    common_info['menu_string'] = kwargs.get('menu_string')
    common_info['filter_dict'] = filter_dict
    common_info['title'] = title_dict['task']
    common_info['html_url'] = 'my/my_task.html'
    common_info['employee_obj'] = employee_obj
    return base.table_obj_list(request, 'reposition', 'mytask', common_info)


# 为模态框传数据
# 显示订单对应业务步骤
@login_required
# @permission
def order_business(request, id, *args, **kwargs):
    """
    :param request:
    :param id: 订单id
    :param args:
    :param kwargs:
    :return:
    """
    if request.method == 'GET':
        order_obj = models.Orders.objects.filter(id=id).first()

        process_step_obj = models.ProcessStep.objects.filter(p_name_id=order_obj.p_business_id) \
            .values('process_name', 'name').order_by('number').all()
        result_dict['data'] = list(process_step_obj)
        process_obj = models.Process.objects.filter(order_id=id).values('process_name',
                                                                        'step_name',
                                                                        'employee_name',
                                                                        'date').order_by('date').all()
        result_dict['tbbody'] = list(process_obj)
        result_dict['employee'] = request.session.get('user_info')['employee_id']
        result_dict['employee_name'] = request.session.get('user_info')['name']
    return JsonResponse(result_dict, safe=False)


# 订单的业务步骤更改
@login_required
# @permission
def order_business_add(request, *args, **kwargs):
    if request.method == 'POST':
        form_obj = OrderBusinessAddForm(data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            employee_id = request.POST.get('employee')
            # 判断该订单的下一个步骤是不是本人
            if employee_id != request.session.get('user_info')['employee_id']:
                # 我的任务的id
                nid = request.POST.get('nid')
                mytask_obj = models.MyTask.objects.filter(id=nid).first()
                mytask_obj.status = 1
                mytask_obj.save()
                data_dict = {
                    'order_id': mytask_obj.order_id,
                    'employee_id': employee_id,
                    'order_serice_id': mytask_obj.order_serice_id,
                    'ctime': datetime.now()
                }

                models.MyTask.objects.create(**data_dict)
            order_id = request.POST.get('order')
            step_name = request.POST.get('step_name')
            order_obj = models.Orders.objects.filter(id=order_id).first()
            process_message_send(order_obj, step_name, employee_id)
            result_dict['status'] = 200
            result_dict['message'] = '添加成功'
        else:
            result_dict['status'] = 801
            result_dict['message'] = list(form_obj.errors.values())[0][0]

    return JsonResponse(result_dict)


@login_required
@permission
def client(request, *args, **kwargs):
    common_info = {}
    common_info['menu_string'] = kwargs.get('menu_string')
    common_info['title'] = title_dict['client']
    common_info['add_url'] = 'my_client_add'
    common_info['edit_url'] = 'my_client_edit'

    return base.table_obj_list(request, 'reposition', 'clientinfo', common_info)


@login_required
@permission
def client_add(request, *args, **kwargs):
    common_info = {}
    common_info['title'] = title_dict['client_add']
    common_info['redirect_url'] = 'my_client'
    common_info['return_link'] = 'my_client'
    common_info['menu_string'] = kwargs.get('menu_string')
    return base.table_obj_add(request, 'reposition', 'clientinfo', common_info)


# @login_required
@permission
def client_edit(request, nid, *args, **kwargs):
    common_info = {}
    common_info['obj_id'] = nid
    common_info['title'] = title_dict['client_edit']
    common_info['redirect_url'] = 'my_client'
    common_info['return_link'] = 'my_client'
    common_info['menu_string'] = kwargs.get('menu_string')
    common_info['html_url'] = 'general_edit_index.html'
    return base.table_obj_change(request, 'reposition', 'clientinfo', common_info)
