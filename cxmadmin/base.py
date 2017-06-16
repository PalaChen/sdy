from django.shortcuts import render, redirect
from cxmadmin import app_setup
from reposition import models
from cxmadmin.admin import site
from cxmadmin.form_handle import create_dynamic_model_form
from django import conf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

app_setup.cxmadmin_auto_discover()


# 过滤出符合条件的数据
def get_filter_result(request, querysets):
    """
    从页面中筛选条件
    :param request:
    :param querysets:
    :return:
    """
    filter_conditions = {}
    for key, val in request.GET.items():
        if key in ('_page', '_o', '_q'): continue
        if val:
            filter_conditions[key] = val

    # print("filter_conditions", filter_conditions)
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
            current_ordered_column[orderby_key] = orderby_index
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
        # print(q.children)
        return querysets.filter(q)
    return querysets


def table_obj_list(request, app_name, model_name, common_dict):
    """
    从site实例总取出指定app名字对应的model_name里的数据返回给前端
    :param request: 视图的request参数
    :param app_name: app名字
    :param model_name: 表对应的类名 小写
    :param common_info: 常用信息
    :return:
    """
    # {'app名字':{数据表的类名：注册的内存地址}}
    # print("app_name,model_name:",site.enabled_admins[app_name][model_name])

    admin_class = site.enabled_admins[app_name][model_name]
    filter_dict = common_dict.get('filter_dict')
    if not filter_dict:
        # 读取所有数据
        querysets = admin_class.model.objects.all()
    else:
        querysets = admin_class.model.objects.filter(**filter_dict).all()
    # 筛选字段
    querysets, filter_condtions = get_filter_result(request, querysets)
    admin_class.filter_condtions = filter_condtions
    # print('querysets-->', querysets)

    # 搜索查询结果
    querysets = get_serached_result(request, querysets, admin_class)
    # 把搜索的值传给admin_class
    admin_class.search_key = request.GET.get('_q', '')

    # 排序后的结果和当前被排序的列的字段
    querysets, sorted_column = get_orderby_result(request, querysets, admin_class)

    # 分页
    paginator = Paginator(querysets, 10)
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


    # print("admin class",admin_class.model )
    html_url = common_dict.get('html_url')
    if not html_url:
        html_url = 'general_index.html'
    return render(request, html_url, {'querysets': querysets,
                                      'admin_class': admin_class,
                                      'sorted_column': sorted_column,
                                      'menu_string': common_dict['menu_string'],
                                      'common_info': common_dict,
                                      })


def table_obj_change(request, app_name, model_name, common_info):
    # 修改数据
    admin_class = site.enabled_admins[app_name][model_name]
    model_form = create_dynamic_model_form(admin_class)
    admin_class.return_link = common_info['return_link']
    obj = admin_class.model.objects.get(id=common_info['obj_id'])
    # return admin_class, model_form, obj
    if request.method == 'GET':
        form_obj = model_form(instance=obj)
    elif request.method == "POST":
        form_obj = model_form(instance=obj, data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(common_info['redirect_url'])
    admin_class.app_name = app_name
    admin_class.model_name = model_name
    return render(request, common_info['html_url'], {'form_obj': form_obj,
                                                     'common_info': common_info,
                                                     'admin_class': admin_class})


def table_obj_add(request, app_name, model_name, common_info):
    admin_class = site.enabled_admins[app_name][model_name]
    model_form = create_dynamic_model_form(admin_class, form_add=True)
    admin_class.return_link = common_info['return_link']
    if request.method == 'GET':
        form_obj = model_form()
    elif request.method == 'POST':
        form_obj = model_form(data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(common_info['redirect_url'])

    html_url = common_info.get('html_url')
    if not html_url:
        html_url = 'general_add_index.html'

    return render(request, html_url, {'form_obj': form_obj,
                                      'common_info': common_info,
                                      'admin_class': admin_class})
