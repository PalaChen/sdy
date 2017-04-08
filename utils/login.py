from django.shortcuts import redirect
from django.urls import reverse


def login_required(func):
    def inner(request, *args, **kwargs):
        if request.session.get('user_info'):
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))

    return inner
