from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from reposition import models
from django.db import connection, connections
from utils.login_admin import login_required, permission
from cxmadmin import base
from django.views.decorators.csrf import csrf_exempt
from backend.forms.org import PositionForm,Permission2Action2roleForm

result_dict = {'status': 200, 'message': None, 'data': None}
title_dict = {'position_index': '组织机构',
              'roles': '职位管理',
              'position_edit': '职位修改',
              'assign': '权限分配',
              'employees': '员工管理',
              'employees_add': '添加员工',
              'employees_edit': '员工信息修改'}


def get_menu_dict():
    cursor = connection.cursor()
    cursor.execute(
        """SELECT t.*,t1.counts FROM (SELECT m.`id`,m.`caption` ,p.id AS p_id,p.`caption` AS p_caption FROM permission AS p, menu AS m WHERE p.`menu_id`=m.`id`) AS t,(SELECT COUNT(caption) AS counts,menu_id FROM permission GROUP BY menu_id) AS t1 WHERE t.id =t1.menu_id""")
    menu_list = cursor.fetchall()
    munu_dict = {}
    # print(menu_list)
    for line in menu_list:
        if line[0] in munu_dict.keys():
            munu_dict[line[0]][1]['menu'].append((line[2], line[3]))
        else:
            munu_dict[line[0]] = [({'number': line[4], 'name': line[1]}), ({'menu': [(line[2], line[3])]})]
    return munu_dict


# 职位信息
@login_required
def position_index(request, *args, **kwargs):
    common_info = {}
    common_info['menu_string'] = kwargs.get('menu_string')
    common_info['title'] = title_dict['position_index']
    common_info['edit_url'] = 'position_edit'
    common_info['html_url'] = 'organization/org_position.html'
    common_info['department_obj'] = models.Department.objects.all()
    common_info['form_obj'] = PositionForm()
    return base.table_obj_list(request, 'reposition', 'position', common_info)


# 部门添加
@login_required
def deparment_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if len(name) <= 30:
            models.Department.objects.create(name=name)
            result_dict['message'] = '部门添加成功'
        else:
            result_dict['status'] = 801
            result_dict['message'] = '长度超过30个字符'
    return JsonResponse(result_dict)


# 部门修改
@csrf_exempt
@login_required
def deparment_edit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        id = request.POST.get('id')
        department_obj = models.Department.objects.filter(id=id).first()
        if department_obj:
            department_obj.name = name
            department_obj.save()
            result_dict['message'] = '部门修改成功'
        else:
            result_dict['status'] = 801
            result_dict['message'] = '长度超过30个字符'
    return JsonResponse(result_dict)


# 部门删除
@csrf_exempt
@login_required
def deparment_del(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        department_obj = models.Department.objects.filter(id=id).first()
        if department_obj:
            models.Department.objects.filter(id=id).delete()
            result_dict['message'] = '部门删除成功'
        else:
            result_dict['status'] = 801
            result_dict['message'] = '非法操作'
    return JsonResponse(result_dict)


# 职位增加
@login_required
def position_add(request):
    if request.method == 'POST':
        position_form = PositionForm(data=request.POST)
        if position_form.is_valid():
            position_form.save()
            result_dict['message'] = '职位添加成功'
        else:
            result_dict['status'] = 801
            result_dict['message'] = list(position_form.errors.values())[0][0]
    else:
        result_dict['status'] = 801
        result_dict['message'] = '非法操作'
    return JsonResponse(result_dict)


# 职位修改
@login_required
def position_edit(request, obj_id, *args, **kwargs):
    common_info = {}
    common_info['obj_id'] = obj_id
    common_info['html_url'] = 'organization/org_position_edit.html'
    common_info['redirect_url'] = 'org_position'
    common_info['return_link'] = 'org_position'
    common_info['title'] = title_dict['position_edit']
    common_info['department_obj'] = models.Department.objects.all()
    return base.table_obj_change(request, 'reposition', 'position', common_info)


# 权限分配
@login_required
def assign(req, id):
    munu_dict = get_menu_dict()
    action_obj = models.Action.objects.all()
    models.Permission2Action2Role.objects.filter()
    # form_obj=Permission2Action2roleForm(instance=)
    if req.method == 'POST':
        permisssion_list = req.POST.getlist('permission_id')
        action_list = req.POST.getlist('action_id')
        start_number = 0
        for i in range(len(permisssion_list)):
            try:
                permission_id = permisssion_list.pop(0)
            except IndexError:
                break
            for l in range(len(action_list)):
                action = action_list.pop(0)
                if start_number == 0:
                    action_id = action
                    start_number = 1
                else:
                    if int(action) != 1:
                        action_id = action
                    else:
                        start_number = 0
                        permission_id = permisssion_list.pop(0)
                        action_id = action
                        obj = models.Permission2Action.objects.filter(action_id=action_id,
                                                                      permission_id=permission_id).first()
                        models.Permission2Action2Role.objects.create(p2a=obj, role_id=id)
                        break
                obj = models.Permission2Action.objects.filter(action_id=action_id, permission_id=permission_id).first()
                models.Permission2Action2Role.objects.create(p2a=obj, role_id=id)

    return render(req, 'organization/assign.html', {'title': title_dict['assign'],
                                                    'munu_dict': munu_dict,
                                                    'action_obj': action_obj,
                                                    })


def bind_permission(req):
    munu_dict = get_menu_dict()
    action_obj = models.Action.objects.all()
    if req.method == 'POST':
        permisssion_list = req.POST.getlist('permission_id')
        action_list = req.POST.getlist('action_id')
        data = {}
        start_number = 0
        for i in range(len(permisssion_list)):
            try:
                data['permission_id'] = permisssion_list.pop(0)
            except IndexError:
                break
            for l in range(len(action_list)):
                action = action_list.pop(0)
                if start_number == 0:
                    data['action_id'] = action
                    start_number = 1
                    models.Permission2Action.objects.create(**data)
                else:
                    if int(action) != 1:
                        data['action_id'] = action
                        models.Permission2Action.objects.create(**data)
                    else:
                        start_number = 0
                        data['permission_id'] = permisssion_list.pop(0)
                        data['action_id'] = action
                        models.Permission2Action.objects.create(**data)
                        break

    return render(req, 'organization/assign.html', {'title': title_dict['assign'],
                                                    'munu_dict': munu_dict,
                                                    'action_obj': action_obj,
                                                    })


def roles(req):
    role_obj = models.Role.objects.all()
    return render(req, 'organization/roles.html', {'title': title_dict['roles'],
                                                   'role_obj': role_obj,})


@login_required
def employees(request, *args, **kwargs):
    common_info = {}
    common_info['menu_string'] = kwargs.get('menu_string')
    common_info['title'] = title_dict['employees']
    common_info['add_url'] = 'org_employees_add'
    common_info['edit_url'] = 'org_employees_edit'
    common_info['html_url'] = 'organization/org_employee.html'
    common_info['department_obj'] = models.Department.objects.all()
    return base.table_obj_list(request, 'reposition', 'employees', common_info)


# @login_required
def employees_add(request, *args, **kwargs):
    common_info = {}
    common_info['menu_string'] = kwargs.get('menu_string')
    common_info['title'] = title_dict['employees_add']
    common_info['redirect_url'] = 'org_employees'
    common_info['return_link'] = 'org_employees'
    common_info['html_url'] = 'organization/org_employee_add.html'
    common_info['department_obj'] = models.Department.objects.all()
    return base.table_obj_add(request, 'reposition', 'employees', common_info)


@login_required
def employees_edit(request, obj_id, *args, **kwargs):
    common_info = {}
    common_info['title'] = title_dict['employees_edit']
    common_info['menu_string'] = kwargs.get('menu_string')
    common_info['obj_id'] = obj_id
    common_info['redirect_url'] = 'org_employees'
    common_info['return_link'] = 'org_employees'
    common_info['html_url'] = 'organization/org_employee_edit.html'
    common_info['department_obj'] = models.Department.objects.all()
    return base.table_obj_change(request, 'reposition', 'employees', common_info)
