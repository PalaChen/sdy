from django.shortcuts import render, redirect
from utils.login_admin import login_required, permission
from cxmadmin import base

title_dict = {'user': '全部客户', 'users_add': '添加客户',
              'user_edit': '客户信息修改',
              'users_consultation':'主页用户查询',}


#
@login_required
@permission
def user(request, *args, **kwargs):
    common_info = {}
    common_info['menu_string'] = kwargs.get('menu_string')
    common_info['order'] = {}
    common_info['add_url'] = 'users_add'
    common_info['title'] = title_dict['user']
    common_info['edit_url'] = 'users_edit'
    return base.table_obj_list(request, 'reposition', 'users', common_info)


@login_required
@permission
def users_add(request, *args, **kwargs):
    common_info = {}
    common_info['menu_string'] = kwargs.get('menu_string')
    common_info['html_url'] = 'general_add_index.html'
    common_info['redirect_url'] = 'users_all'
    common_info['return_link'] = 'users_all'
    common_info['title'] = title_dict['users_add']
    return base.table_obj_add(request, 'reposition', 'users', common_info)
    # admin_class, model_form = admin.table_obj_add(request, 'reposition', 'users')
    # admin_class.return_link = 'users_all'
    # if request.method == 'GET':
    #     form_obj = model_form()
    # elif request.method == 'POST':
    #     form_obj = model_form(data=request.POST)
    #     if form_obj.is_valid():
    #         form_obj.save()
    #         return redirect("users_all")
    # return render(request, 'general_add_index.html', {'title': title_dict['users_add'],
    #                                                   'form_obj': form_obj,
    #                                                   'admin_class': admin_class})


@login_required
@permission
def users_edit(request, obj_id, *args, **kwargs):
    common_info = {}
    common_info['menu_string'] = kwargs.get('menu_string')
    common_info['obj_id'] = obj_id
    common_info['html_url'] = 'users/user_edit.html'
    common_info['redirect_url'] = 'users_all'
    common_info['return_link'] = 'users_all'
    common_info['title'] = title_dict['user_edit']
    return base.table_obj_change(request, 'reposition', 'users', common_info)


@login_required
# @permission
def recommend(request, *args, **kwargs):
    menu_string = kwargs.get('menu_string')
    querysets, admin_class, sorted_column = base.table_obj_list(request, 'reposition', 'users')
    return render(request, 'general_index.html', {'querysets': querysets,
                                                  'admin_class': admin_class,
                                                  'sorted_column': sorted_column,
                                                  'menu_string': menu_string,
                                                  'title': title_dict['user']
                                                  })

@login_required
@permission
def users_consultation(request, *args, **kwargs):
    common_info = {}
    common_info['menu_string'] = kwargs.get('menu_string')
    common_info['title'] = title_dict['users_consultation']
    return base.table_obj_list(request, 'reposition', 'userconsultation', common_info)