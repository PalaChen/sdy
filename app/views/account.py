from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from app.forms import account
from reposition import models, model_query, model_update, model_add
from utils.check_code import create_validate_code
import io
import datetime
from django.utils import timezone

result_dict = {'status': True, 'message': None, 'data': None,}


def login(req):
    form = account.LoginForm(req.POST or None)
    error = ''
    if req.method == 'POST':
        form = account.LoginForm(req.POST)
        if form.is_valid():
            phone = req.POST.get('phone')
            res = model_query.login_user_query(form)
            if res:
                print(2222222)
                ret = redirect(reverse('web_index'))
                ret.set_cookie('user', phone, max_age=3600,
                               expires=datetime.datetime.utcnow() + datetime.timedelta(5))
                req.session['user_info'] = {'phone': phone, 'id': res['id'], 'name': res['name']}
                req.session['is_login'] = 'true'
                return ret
            else:

                error = '账号密码输入有误，请重新输入'
        else:
            error = list(form.errors.values())[0][0]
    return render(req, 'login.html', {'form': form, 'error': error})


def login_ajax(request):
    form = account.LoginForm(request.POST or None)

    if request.method == 'POST':
        form = account.LoginForm(request.POST)
        if form.is_valid():
            phone = request.POST.get('phone')
            res = model_query.login_user_query(form)
            if res:
                ret = redirect(reverse('web_index'))
                ret.set_cookie('user', phone, max_age=3600,
                               expires=datetime.datetime.utcnow() + datetime.timedelta(5))
                request.session['user_info'] = {'phone': phone, 'id': res['id'], 'name': res['name']}
                request.session['is_login'] = 'true'
            else:
                result_dict['status'] = False
                result_dict['message'] = '账号密码输入有误，请重新输入'
        else:
            result_dict['status'] = False
            result_dict['message'] = list(form.errors.values())[0][0]
    return JsonResponse(result_dict)


def logout(req):
    del req.session['user_info']
    del req.session['is_login']
    return redirect('/')


def register(request):
    """
    注册
    :param req:
    :return:
    """
    form_obj = account.RegisterForm(request.POST or None)
    if request.method == 'GET':
        return render(request, 'register.html', {'form': form_obj})

    elif request.method == 'POST':
        if form_obj.is_valid():
            data = form_obj.cleaned_data
            form_obj, res = register_generate(data, request, form_obj, 'reister')
            if not res:
                res_obj = model_add.Add_info(models.Users, data)
                if res_obj:
                    request.session['user_info'] = {'phone': res_obj.phone, 'id': res_obj.id,
                                                    'name': res_obj.name}
                    request.session['is_login'] = 'true'
                    return redirect(reverse('web_index'))
                else:
                    form_obj.errors['phone'] = ['手机号码已存在', ]
    print(form_obj.errors)
    return render(request, 'register.html', {'form': form_obj,})


def register_ajax(request):
    form = account.RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data
            res_obj = register_generate(data, request, 'register', result_dict)
            if not isinstance(res_obj, dict):
                if res_obj:
                    request.session['user_info'] = {'phone': res_obj.phone, 'id': res_obj.id, 'name': res_obj.name}
                    request.session['is_login'] = 'true'
                    return JsonResponse(result_dict)
                else:
                    result_dict['message'] = '手机号码已存在'
        else:
            result_dict['message'] = list(form.errors.values())[0][0]
    result_dict['status'] = False
    return JsonResponse(result_dict)


def forgetpass(request):
    form_obj = account.ForgetPassForm(request.POST or None)
    if form_obj.is_valid():
        data = form_obj.cleaned_data
        del data['password2']
        form_obj, res = register_generate(data, request, form_obj, 'forgetpass')
        if not res:
            return render(request, 'forgetpass_2.html')
    return render(request, 'forgetpass.html', {'form': form_obj})


def register_generate(data, request, form, type):
    code = data.pop('code')
    verify_code = data.pop('verify_code')
    phone = data['phone']
    del data['password2']
    verify_info = models.MessagesVerifyCode.objects.filter(m_phone=phone, ) \
        .values_list('m_verifycode', 'm_send_date').order_by('-m_send_date').first()
    # 防止用户输入的手机号码和系统中发送短信手机号码不一致
    if verify_info:
        # 图片验证码判断
        if code.upper() == request.session.get('checkCode').upper():
            # 短信验证码判断
            if int(verify_code) == verify_info[0]:
                # 短信验证码时效性验证
                if (timezone.now() - verify_info[1]).seconds <= 1800:
                    if type == 'register':
                        return form, None
                    else:
                        models.Users.objects.filter(phone=phone).update(password=data['password'])
                        return form, None
                else:
                    form.errors['verify_code'] = ['短信验证码超时，请重新获取', ]
            else:
                form.errors['verify_code'] = ['短信验证码输入错误，请重新输入', ]
        else:
            form.errors['code'] = ['验证码输入错误', ]
    else:
        form.errors['verify_code'] = ['接受短信的手机号码和输入对的手机号码不一致', ]

    return form, True


def register_ajax_generate(data, request, type, result_dict):
    del data['password2']
    code = data.pop('code')
    verify_code = data.pop('verify_code')
    phone = data['phone']
    verify_info = models.MessagesVerifyCode.objects.filter(m_phone=phone, ) \
        .values_list('m_verifycode', 'm_send_date').order_by('-m_send_date').first()
    # 防止用户输入的手机号码和系统中发送短信手机号码不一致
    if verify_info:
        # 图片验证码判断
        if code.upper() == request.session.get('checkCode').upper():
            # 短信验证码判断
            if int(verify_code) == verify_info[0]:
                # 短信验证码时效性验证
                if (timezone.now() - verify_info[1]).seconds <= 1800:
                    if type == 'register':
                        res_obj = model_add.Add_info(models.Users, **data)
                        return res_obj
                    else:
                        models.Users.objects.filter(phone=phone).update(password=data['password'])
                        return
                else:
                    result_dict['message'] = '短信验证码超时，请重新获取'
            else:
                result_dict['message'] = '短信验证码输入错误，请重新输入'
        else:
            result_dict['message'] = '验证码输入错误'
    else:
        result_dict['message'] = '接受短信的手机号码和输入对的手机号码不一致'
    return result_dict


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
