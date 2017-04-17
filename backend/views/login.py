from django.shortcuts import render, HttpResponse, redirect, reverse
from backend.forms import forms
from reposition import model_query
import datetime
from utils.login_admin import MenuHelper

result_dict = {'status': 200, 'message': None, 'data': 'None'}


def login(req):
    form = forms.LoginForm(req.POST or None)
    if req.method == 'POST':
        if form.is_valid():
            obj = model_query.login_employee_query(req.POST)
            if obj:
                ret = redirect(reverse('site_manage'))
                ret.set_cookie('employee_id', obj['id'], max_age=3600,
                               expires=datetime.datetime.utcnow() + datetime.timedelta(5))
                req.session['user_info'] = {'nid': obj['id'], 'email': obj['email'], 'name': obj['name']}
                req.session['employee_id'] = obj['id']
                req.session['is_login'] = True
                MenuHelper(req, obj['email'])
                return ret
        else:
            result_dict['message'] = list(form.errors.values())[0][0]
            result_dict['status'] = False
    return render(req, 'admin_login.html', {'form': form,
                                            'result_dict': result_dict})


def logout(request):
    request.session.clear()
    return redirect('admin_login')
