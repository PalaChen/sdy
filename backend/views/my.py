from django.shortcuts import render, HttpResponse
from utils.login_admin import permission, login_required

title_dict = {'my_task': '我的任务', 'my_client': '我的客户'
              }


@permission
def my_task(req, *args, **kwargs):
    action_list = kwargs.get('action_list')
    menu_string = kwargs.get('menu_string')
    return render(req, 'my/master/base.html', {'menu_string': menu_string,
                                               'title': title_dict['my_task']})


@permission
def my_client(req, *args, **kwargs):
    action_list = kwargs.get('action_list')
    menu_string = kwargs.get('menu_string')
    return render(req, 'my/master/base.html', {'menu_string': menu_string,
                                               'title': title_dict['my_client']})
