from django.shortcuts import render, HttpResponse, redirect, reverse
from backend import forms
from reposition import model_query
import datetime

result_dict = {'status': 200, 'message': None, 'data': 'None'}


def login(req):
    form = forms.LoginForm(req.POST or None)

    if req.method == 'POST':
        if form.is_valid():
            res = model_query.login_employee_query(req.POST)
            if res:
                ret = redirect(reverse('site_manage'))
                ret.set_cookie('employee_id', res[0], max_age=3600,
                               expires=datetime.datetime.utcnow() + datetime.timedelta(5))
                req.session['employee_id'] = res[0]
                req.session['is_login'] = 'true'
                return ret
        else:
            result_dict['message'] = list(form.errors.values())[0][0]
            result_dict['status'] = False
    return render(req, 'admin_login.html', {'form': form,
                                            'result_dict': result_dict})
