from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from cxmadmin import app_setup
from reposition import models
from cxmadmin.admin import site
from cxmadmin.form_handle import create_dynamic_model_form
from django import conf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.db.models import Q
import json

app_setup.cxmadmin_auto_discover()


# print('site---------->', site.enabled_admins)


def app_index(request):
    return render(request, 'cxmadmin/app_index.html', {'site': site})


# 筛选符合条件的字段
def get_filter_result(request, querysets):
    """
    筛选条件
    :param request:
    :param querysets:
    :return:
    """
    filter_conditions = {}
    print('request.GET',request.GET)
    for key, val in request.GET.items():
        if key in ('_page', '_o', '_q'):
            continue
        if val:
            filter_conditions[key] = val

    print("filter_conditions", filter_conditions)
    return querysets.filter(**filter_conditions), filter_conditions


# 输出结果排序
def get_orderby_result(request, querysets, admin_class):
    """
    输出结果排序
    :param request:
    :param querysets:
    :return:
    """
    current_ordered_column = {}
    orderby_index = request.GET.get('_o')

    if orderby_index:
        # 防止传的数据不是数字
        try:
            orderby_key = admin_class.list_display[abs(int(orderby_index))]
            # 为了让前端知道当前排序的列
            current_ordered_column[orderby_key] = orderby_index  # 为了让前端知道当前排序的列
            if orderby_index.startswith('-'):
                orderby_key = '-' + orderby_key
                return querysets.order_by(orderby_key), current_ordered_column
        except ValueError:
            pass
    return querysets, current_ordered_column


# 筛选符合搜索条件的结果
def get_serached_result(request, querysets, admin_class):
    search_key = request.GET.get('_q')
    if search_key:
        q = Q()
        q.connector = 'OR'

        for search_field in admin_class.search_fields:
            q.children.append(("%s__contains" % search_field, search_key))
        print(q.children)
        return querysets.filter(q)
    return querysets


def table_obj_list(request, app_name, model_name):
    """取出指定model里的数据返回给前端"""
    # {'app名字':{数据表的类名：注册的内存地址}}
    # print("app_name,model_name:",site.enabled_admins[app_name][model_name])

    admin_class = site.enabled_admins[app_name][model_name]
    if request.method == "POST":
        print(request.POST)
        # action类型
        selected_action = request.POST.get('action')
        # 获取要删除数据所对应的id
        selected_ids = json.loads(request.POST.get('selected_ids'))
        # print(selected_action, selected_ids)
        # 匹配将要删除的数据
        selected_objs = admin_class.model.objects.filter(id__in=selected_ids)
        # 反射admin_class是否有该功能
        if hasattr(admin_class, selected_action):
            admin_action_func = getattr(admin_class, selected_action)
            # 执行该功能
            admin_action_func(request, selected_objs)
    # 读取所有数据
    querysets = admin_class.model.objects.all()
    # 刷选字段
    querysets, filter_condtions = get_filter_result(request, querysets)
    admin_class.filter_condtions = filter_condtions

    # 搜索查询结果
    querysets = get_serached_result(request, querysets, admin_class)
    # 把搜索的值传给admin_class
    admin_class.search_key = request.GET.get('_q', '')

    # 排序后的结果和当前被排序的列的字段
    querysets, sorted_column = get_orderby_result(request, querysets, admin_class)

    # 分页
    paginator = Paginator(querysets, admin_class.list_per_page)
    page = request.GET.get('_page')
    try:
        querysets = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        querysets = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        querysets = paginator.page(paginator.num_pages)

    # return render(request, 'list.html', {'contacts': contacts})

    admin_class.app_name = app_name
    admin_class.model_name = model_name
    # print("admin class",admin_class.model )

    print('admin_class.actions', admin_class.actions)
    return render(request, 'cxmadmin/table_obj_list.html', {'querysets': querysets,
                                                            'admin_class': admin_class,
                                                            'sorted_column': sorted_column,})


def table_obj_change(request, app_name, model_name, obj_id):
    # 修改数据
    admin_class = site.enabled_admins[app_name][model_name]
    model_form = create_dynamic_model_form(admin_class)
    obj = admin_class.model.objects.get(id=obj_id)
    if request.method == 'GET':
        form_obj = model_form(instance=obj)
    elif request.method == "POST":
        form_obj = model_form(instance=obj, data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect("/cxmadmin/%s/%s/" % (app_name, model_name))
    admin_class.app_name = app_name
    admin_class.model_name = model_name
    return render(request, 'cxmadmin/table_obj_change.html', {'form_obj': form_obj,
                                                              'admin_class': admin_class})


def table_obj_add(request, app_name, model_name):
    admin_class = site.enabled_admins[app_name][model_name]
    model_form = create_dynamic_model_form(admin_class)
    admin_class.app_name = app_name
    admin_class.model_name = model_name

    if request.method == 'GET':
        form_obj = model_form()
    elif request.method == 'POST':
        form_obj = model_form(data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect("/cxmadmin/%s/%s/" % (app_name, model_name))
    return render(request, 'cxmadmin/table_obj_add.html', {'form_obj': form_obj,
                                                           'admin_class': admin_class})


def table_obj_delete(request, app_name, model_name, obj_id):
    admin_class = site.enabled_admins[app_name][model_name]
    obj = admin_class.model.objects.get(id=obj_id)
    admin_class.app_name = app_name
    admin_class.model_name = model_name
    if request.method == 'POST':
        obj.delete()
        return redirect("/cxmadmin/%s/%s/" % (app_name, model_name))
    return render(request, 'cxmadmin/table_obj_delete.html', {'obj': obj,
                                                              'admin_class': admin_class})


def admin_login(request):
    error_msg = ''
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        # print(authenticate(username=email, password=password))
        user = authenticate(username=email, password=password)
        if user:
            print("passed authencation", user)
            login(request, user)

            return redirect(request.GET.get('next', '/cxmadmin/'))
        else:
            error_msg = "错误用户名!"

    return render(request, 'cxmadmin/admin1_login.html', {'error_msg': error_msg})


def admin_logout(request):
    logout(request)
    return redirect("cxmadmin/login/")
