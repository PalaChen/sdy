from django.shortcuts import redirect, HttpResponse
from django.urls import reverse
from utils.menu import MenuHelper
import functools

# @functools.wraps
def login_required(func):
    def inner(request, *args, **kwargs):
        try:
            if request.session.get('is_login'):
                return func(request, *args, **kwargs)
            else:
                return redirect(reverse('admin_login'))
        except AttributeError as e:
            return redirect(reverse('admin_login'))

    return inner

# @functools.wraps
def permission(func):
    def inner(request, *args, **kwargs):
        user_info = request.session.get('user_info')
        if not user_info:
            return redirect('admin_login')
        obj = MenuHelper(request, user_info['email'])
        action_list = obj.actions()
        if not action_list:
            return HttpResponse('无权访问')
        kwargs['menu_string'] = obj.menu_tree()
        kwargs['action_list'] = action_list
        return func(request, *args, **kwargs)

    return inner
