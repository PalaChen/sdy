from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from app.forms import account
from reposition import models, model_query, model_update, model_add
from utils.check_code import create_validate_code
import io
import datetime


def login(req):
    form = account.LoginForm(req.POST or None)

    if req.method == 'POST':
        form = account.LoginForm(req.POST)
        if form.is_valid():
            phone = req.POST.get('phone')
            res = model_query.login_user_query(form)
            if res:
                ret = redirect(reverse('web_index'))
                ret.set_cookie('user', phone, max_age=3600,
                               expires=datetime.datetime.utcnow() + datetime.timedelta(5))
                req.session['user_id'] = res[0]
                req.session['user_info'] = phone
                req.session['is_login'] = 'true'
                return ret

    return render(req, 'login.html', {'form': form})


def register(req):
    """
    注册
    :param req:
    :return:
    """
    form = account.RegisterForm()
    if req.method == 'GET':
        return render(req, 'register.html', {'form': form})
    elif req.method == 'POST':
        form = account.RegisterForm(req.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            if code.upper() == req.session.get('checkCode').upper():
                res = model_add.Add_info(models.Users, form.cleaned_data)
                if res == True:
                    return redirect(reverse('web_index'))
                else:
                    form.errors['phone'] = '手机号码已存在'

            else:
                form.errors['code'] = '验证码输入错误'
    return render(req, 'register.html', {'form': form,
                                         'errors': form.errors})


def get_captcha(req):
    """
    验证码
    :param req:
    :return:
    """
    if req.method == 'GET':
        f = io.BytesIO()
        img, code = create_validate_code()
        img.save(f, 'png')
        req.session['checkCode'] = code
        return HttpResponse(f.getvalue())
