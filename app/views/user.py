from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from app.forms.info import EditProfileForm, EditPhoneForm, EditPwdForm
from reposition import models
from reposition.model_query import order_counts
from utils.login import login_required
from utils.sms_message import send_verification_code
from utils.serialize import DateTypeJSONEncoder
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
res_dict = {
    'status': True,
    'message': None,
    'data': None,
}


@login_required
def index(req):
    user_info = req.session.get('user_info')
    counts_dict = order_counts(user_info['phone'])
    return render(req, 'user/user_index.html', {'title': title['index'],
                                                'user_info': user_info,
                                                'counts_dict': counts_dict,})


@login_required
def order(req):
    user_info = req.session.get('user_info')
    order_obj = models.Orders.objects.filter(phone=user_info['phone']).order_by('-ctime').all()
    counts_dict = order_counts(user_info['phone'])
    return render(req, 'user/order.html', {'order_obj': order_obj,
                                           'user_info': user_info,
                                           'counts_dict': counts_dict,
                                           'title': title['order'],
                                           'id': 0,
                                           })


@login_required
def order_topay(request, nid):
    if request.method == 'GET':
        phone = request.session.get('user_info')['phone']
        order_dict = models.Orders.objects.filter(id=nid, phone=phone).values('order_code').all()
        if order_dict:
            # print(order_dict['order_code'])
            pay_dict = models.OrderPayment.objects.filter(order_code=order_dict['order_code']).values('id').first()
            if pay_dict:
                
                return redirect('shopping_pay', pay_dict['id'])
    return redirect('user_order')


@login_required
def order_query(req, id):
    user_info = req.session.get('user_info')
    phone = user_info['phone']
    id = int(id)
    counts_dict = order_counts(phone)
    if id == 1:
        order_obj = models.Orders.objects.filter(phone=phone, order_state=0).order_by('-ctime').all()
    elif id == 5:
        order_obj = models.Orders.objects.filter(phone=phone, order_state=1).order_by('-ctime').all()
    elif id == 15:
        order_obj = models.Orders.objects.filter(phone=phone, order_state=2).order_by('-ctime').all()
    elif id == 25:
        order_obj = models.Orders.objects.filter(phone=phone, order_state=3).order_by('-ctime').all()
    else:
        return redirect(reverse('user_index'))
    return render(req, 'user/order.html', {'title': title['order'],
                                           'user_info': user_info,
                                           'order_obj': order_obj,
                                           'counts_dict': counts_dict,
                                           'id': id,
                                           })


@login_required
def order_process_query(req, id):
    if req.method == 'GET':
        order_obj = models.Process.objects.filter(order_id=id).values('step_name', 'date').order_by('date').all()
        if order_obj:
            res_dict['data'] = list(order_obj)
        else:
            res_dict['status'] = False
            res_dict['message'] = '暂无数据'

    return JsonResponse(res_dict, encoder=DateTypeJSONEncoder)


@login_required
def info(req):
    form = EditProfileForm(req.POST or None)
    phone = req.session.get('user_info')['phone']
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
            res_dict['message'] = '修改成功'
        else:
            res_dict['status'] = False
            res_dict['message'] = list(form.errors.values())[0][0]

        return JsonResponse(res_dict)

    return render(req, 'user/profile.html', {'title': title['info'],
                                             'form': form,
                                             'user_info': user_info,
                                             })


@login_required
def edit_phone(req):
    form = EditPhoneForm(req.POST or None)
    user_info = req.session.get('user_info')
    phone = user_info['phone']

    if req.method == 'POST':
        if form.is_valid():
            new_phone = req.POST.get('phone')
            password = req.POST.get('password')
            verify_code = req.POST.get('verify_code')
            verify_info = \
                models.MessagesVerifyCode.objects.filter(m_phone=phone, ).values_list('m_verifycode',
                                                                                      'm_send_date').order_by(
                    '-m_send_date').first()
            user_info = models.Users.objects.filter(phone=phone, password=password).first()
            if user_info and verify_info:
                if int(verify_code) == verify_info[0]:
                    if (timezone.now() - verify_info[1]).seconds <= 1800:
                        phone_info = models.Users.objects.filter(phone=new_phone).first()
                        if not phone_info:
                            models.Users.objects.filter(phone=phone).update(phone=new_phone)
                            res_dict['message'] = '修改手机号码成功'
                        else:
                            res_dict['message'] = '该手机号码已被使用'
                    else:
                        res_dict['message'] = '验证码超时，请重新获取'
                else:
                    res_dict['message'] = '验证码输入错误，请重新输入'
            else:
                res_dict['message'] = '非法操作'
        else:
            res_dict['message'] = list(form.errors.values())[0][0]
        res_dict['status'] = False
        return JsonResponse(res_dict)
    return render(req, 'user/edit_phone.html', {'title': title['edit_phone'],
                                                'user_info': user_info})


@login_required
def edit_pwd(req):
    user_info = req.session.get('user_info')
    form = EditPwdForm(req.POST or None)
    if req.method == 'POST':
        if form.is_valid():
            phone = user_info['phone']
            password = req.POST.get('password')
            models.Users.objects.filter(phone=phone).update(password=password)
            res_dict['message'] = '请使用新密码重新登录'
        else:

            res_dict['status'] = False
            res_dict['message'] = list(form.errors.values())[0][0]

        return JsonResponse(res_dict)

    return render(req, 'user/edit_password.html', {'title': title['edit_pwd'],
                                                   'user_info': user_info})


@login_required
def message_unread(req):
    pass


@login_required
def message_read(req):
    pass


def send_verify_code(req):
    if req.method == 'GET':
        phone = req.GET.get('phone')
        type = req.GET.get('type')
        print(phone)
        if phone:
            if len(phone) != 11:
                res_dict['status'] = False
                res_dict['message'] = '手机号码长度不对'
                return JsonResponse(res_dict)

            if not phone.isdigit():
                res_dict['status'] = False
                res_dict['message'] = '请输入正确手机号码'
                return JsonResponse(res_dict)

            if not type:
                type = 'register'

            elif type == 'forgetpass':
                user_obj = models.Users.objects.filter(phone=phone).first()
                if not user_obj:
                    res_dict['status'] = False
                    res_dict['message'] = '该手机号码未注册'
                    return JsonResponse(res_dict)

        else:
            type = 'edit'
            phone = req.session.get('user_info')['phone']

        ret = send_verification_code(phone, type)
        # ret = True
        # if ret:
        return JsonResponse(res_dict)
