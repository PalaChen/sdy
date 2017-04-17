from django.shortcuts import render, redirect, HttpResponse
from reposition import models
from django.db import connection, connections

title_dict = {'index': '系统配置',
              'roles': '职位管理',
              'assign': '权限分配',
              'employees': '员工管理'}


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


def index(req):
    return render(req, 'organization/index.html', {'title': title_dict['assign'],})
    # menu_obj = models.Menu.objects.select_related('permission').all()


def departments(req):
    return HttpResponse('.....')


def assign(req, id):
    munu_dict = get_menu_dict()
    action_obj = models.Action.objects.all()
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
    print(req.POST)
    return render(req, 'organization/roles.html', {'title': title_dict['roles'],
                                                   'role_obj': role_obj,})


def employees(req):
    employee_obj = models.Employees.objects.all()
    return render(req, 'organization/employees.html', {'title': title_dict['employees'],
                                                       'employee_obj': employee_obj,})
