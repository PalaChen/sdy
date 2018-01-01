from django.shortcuts import redirect
from django.urls import reverse


def login_required(func):
    def inner(request, *args, **kwargs):
        user_info = request.session.get('user_info')
        if request.session.get('user_info') and user_info.get('id') and user_info.get('phone'):
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))

    return inner


def wap_login_required(func):
    def inner(request, *args, **kwargs):
        if request.session.get('user_info'):
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse('wap_login'))

    return inner
