from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from reposition import models
from django.db import connection, connections
from utils.login_admin import login_required, permission
from cxmadmin import base
from django.views.decorators.csrf import csrf_exempt
from backend.forms.org import PositionForm, Permission2Action2roleForm

result_dict = {'status': 200, 'message': None, 'data': None}
title_dict = {'position_index': '组织机构',
              'roles': '权限角色',
              'roles_add': '增加角色',
              'roles_edit': '修改角色',
              'position_edit': '职位修改',
              'assign': '权限分配',
              'employees': '员工管理',
              'employees_add': '添加员工',
              'employees_edit': '员工信息修改'}


def get_menu_dict():
    cursor = connection.cursor()
    cursor.execute(
        """SELECT t.*,t1.counts FROM (SELECT m.`id`,m.`caption` ,p.id AS p_id,p.`caption` AS p_caption FROM permission AS p, menu AS m WHERE p.`menu_id`=m.`id` AND p.`weight` = 0) AS t,(SELECT COUNT(caption) AS counts,menu_id FROM permission AS p1 WHERE p1.`weight`=0 GROUP BY menu_id) AS t1 WHERE t.id =t1.menu_id""")
    # """SELECT t.*,t1.counts FROM (SELECT m.`id`,m.`caption` ,p.id AS p_id,p.`caption` AS p_caption FROM permission AS p, menu AS m WHERE p.`menu_id`=m.`id`) AS t,(SELECT COUNT(caption) AS counts,menu_id FROM permission GROUP BY menu_id) AS t1 WHERE t.id =t1.menu_id""")
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
@permission
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
@permission
def deparment_add(request, *args, **kwargs):
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
@permission
def deparment_edit(request, *args, **kwargs):
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
@permission
def deparment_del(request, *args, **kwargs):
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
@permission
def position_add(request, *args, **kwargs):
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
@permission
def position_edit(request, obj_id, *args, **kwargs):
    common_info = {}
    common_info['obj_id'] = obj_id
    common_info['html_url'] = 'organization/org_position_edit.html'
    common_info['redirect_url'] = 'org_position'
    common_info['return_link'] = 'org_position'
    common_info['title'] = title_dict['position_edit']
    common_info['department_obj'] = models.Department.objects.all()
    return base.table_obj_change(request, 'reposition', 'position', common_info)


# # 员工分配角色
# def assign_role(request,id,*args,**kwargs):
#     role_obj=models.Role.objects.all()
#     return render(request,'organization/assign_role.html',{'role_obj':role_obj})
#


# 角色权限分配
@login_required
@permission
def assign(req, id, *args, **kwargs):
    menu_string = kwargs.get('menu_string')
    munu_dict = get_menu_dict()
    permission_obj = models.Permission.objects.filter(menu_id__isnull=True, weight=0).all()
    permission_action_obj = models.Permission2Action.objects.all()
    if req.method == 'POST':
        action_list = req.POST.getlist('action_id')
        for l in action_list:
            models.Permission2Action2Role.objects.create(p2a_id=l, role_id=id)
        return redirect('organization_roles')

    return render(req, 'organization/assign.html', {'title': title_dict['assign'],
                                                    'munu_dict': munu_dict,
                                                    'permission_obj': permission_obj,
                                                    'menu_string': menu_string,
                                                    'permission_action_obj': permission_action_obj,
                                                    })


def bind_permission(req):
    munu_dict = get_menu_dict()
    permission_obj = models.Permission.objects.all()
    action_obj = models.Action.objects.all()
    # 所有菜单绑定action
    # for line in permission_obj:
    #     for i in [1, 2, 3, 4]:
    #         data = {'permission': line, 'action_id': i}
    #         models.Permission2Action.objects.create(**data)

    return render(req, 'organization/assign.html', {'title': title_dict['assign'],
                                                    'munu_dict': munu_dict,
                                                    'action_obj': action_obj,
                                                    })


@login_required
@permission
def roles(request, *args, **kwargs):
    common_info = {}
    common_info['menu_string'] = kwargs.get('menu_string')
    common_info['title'] = title_dict['roles']
    common_info['add_url'] = 'organization_roles_add'
    common_info['edit_url'] = 'organization_roles_edit'
    common_info['html_url'] = 'organization/org_roles.html'
    common_info['department_obj'] = models.Department.objects.all()
    return base.table_obj_list(request, 'reposition', 'role', common_info)


@login_required
@permission
def roles_add(request, *args, **kwargs):
    common_info = {}
    common_info['menu_string'] = kwargs.get('menu_string')
    common_info['title'] = title_dict['roles_add']
    common_info['redirect_url'] = 'organization_roles'
    common_info['return_link'] = 'organization_roles'
    common_info['html_url'] = 'organization/org_roles_add.html'
    common_info['department_obj'] = models.Department.objects.all()
    return base.table_obj_add(request, 'reposition', 'role', common_info)


@login_required
@permission
def roles_edit(request, role_id, *args, **kwargs):
    common_info = {}
    common_info['title'] = title_dict['roles_edit']
    common_info['menu_string'] = kwargs.get('menu_string')
    common_info['obj_id'] = role_id
    common_info['redirect_url'] = 'organization_roles'
    common_info['return_link'] = 'organization_roles'
    common_info['html_url'] = 'organization/org_roles_edit.html'
    common_info['department_obj'] = models.Department.objects.all()
    return base.table_obj_change(request, 'reposition', 'role', common_info)


@login_required
@permission
def employees(request, *args, **kwargs):
    common_info = {}
    common_info['menu_string'] = kwargs.get('menu_string')
    common_info['title'] = title_dict['employees']
    common_info['add_url'] = 'org_employees_add'
    common_info['edit_url'] = 'org_employees_edit'
    common_info['html_url'] = 'organization/org_employee.html'
    common_info['department_obj'] = models.Department.objects.all()
    return base.table_obj_list(request, 'reposition', 'employees', common_info)


@login_required
@permission
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
@permission
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
