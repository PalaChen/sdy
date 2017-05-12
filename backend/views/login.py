from django.shortcuts import render, HttpResponse, redirect, reverse
from django.http import JsonResponse
from backend.forms import forms
from reposition import model_query, models
import datetime
from utils.login_admin import MenuHelper
from utils.login_admin import login_required, permission

result_dict = {'status': 200, 'message': None, 'data': 'None'}


def login(req):
    form = forms.LoginForm(req.POST or None)
    error = ''
    if req.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data

            obj = model_query.login_employee_query(data)
            if obj:
                ret = redirect(reverse('site_manage'))
                ret.set_cookie('employee_id', obj['id'], max_age=3600,
                               expires=datetime.datetime.utcnow() + datetime.timedelta(5))
                req.session['user_info'] = {'employee_id': obj['id'], 'email': obj['email'], 'name': obj['name']}
                # req.session['employee_id'] = obj['id']
                req.session['is_login'] = True
                MenuHelper(req, obj['email'])
                return ret
            else:
                error = '账号密码错误'
        else:
            error = list(form.errors.values())[0][0]
    return render(req, 'admin_login.html', {'form': form,
                                            'error': error})


def logout(request):
    request.session.clear()
    return redirect('admin_login')

# @login_required
# @permission
# def get_menu(request, *args, **kwargs):
#     menu_string = kwargs.get('menu_string')
#     return HttpResponse(menu_string)
