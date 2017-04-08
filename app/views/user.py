from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from app.forms.info import EditProfileForm, EditPhoneForm, EditPwdForm
from reposition import models
from reposition.model_query import order_counts
from utils.login import login_required
from utils.sms_message import send_verification_code
from datetime import datetime, timezone
from django.utils import timezone
import json

title = {
    "index": '消息中心',
    'order': '订单记录',
    'info': '基本资料',
    'edit_phone': '修改手机号码',
    'edit_pwd': '修改密码',
}
res = {
    'status': True,
    'message': None,
    'data': None,
}


@login_required
def index(req):
    phone = req.session.get('user_info')
    pending_pay, to_be_service, in_service, service_completed = order_counts(phone)
    return render(req, 'user/user_index.html', {'title': title['index'],
                                                'pending_pay': pending_pay,
                                                'to_be_service': to_be_service,
                                                'in_service': in_service,
                                                'service_completed': service_completed,})


@login_required
def order(req):
    phone = req.session.get('user_info')
    order_obj = models.Orders.objects.filter(phone=phone).all()
    pending_pay, to_be_service, in_service, service_completed = order_counts(phone)
    return render(req, 'user/order.html', {'order_obj': order_obj,
                                           'pending_pay': pending_pay,
                                           'to_be_service': to_be_service,
                                           'in_service': in_service,
                                           'service_completed': service_completed,
                                           'title': title['order'],
                                           'id': 0,
                                           })


@login_required
def order_query(req, id):
    phone = req.session.get('user_info')
    id = int(id)
    pending_pay, to_be_service, in_service, service_completed = order_counts(phone)
    if id == 1:
        order_obj = models.Orders.objects.filter(phone=phone, order_state='待付款').all()
    elif id == 5:
        order_obj = models.Orders.objects.filter(phone=phone, order_state='待服务').all()
    elif id == 15:
        order_obj = models.Orders.objects.filter(phone=phone, order_state='服务中').all()
    elif id == 25:
        order_obj = models.Orders.objects.filter(phone=phone, order_state='服务完成').all()
    else:
        return redirect(reverse('user_index'))
    return render(req, 'user/order.html', {'title': title['order'],
                                           'order_obj': order_obj,
                                           'pending_pay': pending_pay,
                                           'to_be_service': to_be_service,
                                           'in_service': in_service,
                                           'service_completed': service_completed,
                                           'id': id,
                                           })


@login_required
def order_process_query(req, id):
    if req.method == 'GET':
        order_boj = models.Process.objects.filter(order_id=id).values_list('process_name', 'step_name',
                                                                           'date').order_by('date')
        if order_boj:
            print(order_boj)
            # res['data'] = order_boj
            return JsonResponse(res)
        # 如果没有进展信息，返回默认值
        else:
            res['message'] = '确认订单，等待分配'
            return JsonResponse(res)


@login_required
def info(req):
    form = EditProfileForm(req.POST or None)
    phone = req.session.get('user_info')
    user_info = models.Users.objects.filter(phone=phone).values('phone', 'email',
                                                                'name', 'province',
                                                                'city', 'area', 'address').first()
    if req.method == 'POST':
        if form.is_valid():
            email = req.POST.get('email')
            name = req.POST.get('name')
            address = req.POST.get('address')
            know = req.POST.get('know')
            models.Users.objects.filter(phone=phone).update(email=email, name=name, address=address, know=know)
            res['message'] = '修改成功'
        else:
            res['status'] = False
            res['message'] = list(form.errors.values())[0][0]

        return JsonResponse(res)

    return render(req, 'user/profile.html', {'title': title['info'],
                                             'form': form,
                                             'user_info': user_info,
                                             })


@login_required
def edit_phone(req):
    form = EditPhoneForm(req.POST or None)
    phone = req.session.get('user_info')

    if req.method == 'POST':
        if form.is_valid():
            new_phone = req.POST.get('phone')
            password = req.POST.get('password')
            verify_code = req.POST.get('verify_code')
            verify_info = \
                models.MessagesVerifyCode.objects.filter(m_phone=phone,
                                                         ).values_list('m_verifycode',
                                                                       'm_send_date').order_by('-m_send_date').first()
            user_info = models.Users.objects.filter(phone=phone, password=password).first()
            if user_info:
                if int(verify_code) == verify_info[0]:
                    if (timezone.now() - verify_info[1]).seconds <= 1800:
                        phone_info = models.Users.objects.filter(phone=new_phone).first()
                        if not phone_info:
                            models.Users.objects.filter(phone=phone).update(phone=new_phone)
                            res['message'] = '修改手机号码成功'
                        else:
                            res['message'] = '该手机号码已被使用'
                    else:
                        res['message'] = '验证码超时，请重新获取'
                else:
                    res['message'] = '验证码输入错误，请重新输入'
            else:
                res['message'] = '非法操作'
        else:
            res['message'] = list(form.errors.values())[0][0]
        res['status'] = False
        return JsonResponse(res)
    return render(req, 'user/edit_phone.html', {'title': title['edit_phone']})


@login_required
def edit_pwd(req):
    form = EditPwdForm(req.POST or None)
    if req.method == 'POST':
        if form.is_valid():
            phone = req.session.get('user_info')
            password = req.POST.get('password')
            models.Users.objects.filter(phone=phone).update(password=password)
            res['message'] = '请使用新密码重新登录'
        else:
            print(form.errors)
            res['status'] = False
            res['message'] = list(form.errors.values())[0][0]

        return JsonResponse(res)

    return render(req, 'user/edit_password.html', {'title': title['edit_pwd']})


@login_required
def message_unread(req):
    pass


@login_required
def message_read(req):
    pass


def send_verify_code(req):
    if req.method == 'GET':
        phone = req.session.get('user_info')
        # ret = send_verification_code(phone)
        ret = True
        if ret:
            return JsonResponse(res)
