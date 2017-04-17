from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse

from reposition import models
from utils.login_admin import login_required, permission

title_dict = {'manage': '任务管理', 'order': '订单管理', 'order_add': '订单添加'}


@login_required
@permission
def manage(request, *args, **kwargs):
    action_list = kwargs.get('action_list')
    menu_string = kwargs.get('menu_string')

    return render(request, 'service/manage.html', {'menu_string': menu_string,
                                                   'title': title_dict['manage']})


@login_required
@permission
def order(request, *args, **kwargs):
    action_list = kwargs.get('action_list')
    menu_string = kwargs.get('menu_string')
    order_obj = models.Orders.objects.all().order_by('-ctime')
    return render(request, 'service/order.html', {'menu_string': menu_string,
                                                  'title': title_dict['order']})


@login_required
def order_add(request, *args, **kwargs):
    ction_list = kwargs.get('action_list')
    menu_string = kwargs.get('menu_string')
    return render(request, 'service/order_add.html', {'menu_string': menu_string,
                                                      'title': title_dict['order_add']})
