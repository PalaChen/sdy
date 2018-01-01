from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from app.forms.info import EditProfileForm, EditPhoneForm, EditPwdForm, UserRecommendForm
from reposition import models
from reposition.model_query import order_counts
from utils.login import login_required
from utils.sms_message import send_verification_code
from utils.serialize import DateTypeJSONEncoder
from datetime import datetime, timezone
from django.utils import timezone
from utils.menu import user_info
from django.db.models import Q

import json

title = {
    "index": '消息中心',
    'order': '订单记录',
    'info': '基本资料',
    'edit_phone': '修改手机号码',
    'edit_pwd': '修改密码',
    'coupon': '我的优惠卷',
    'recmomend': '我要推荐',
    'recmomend_count': '推荐人数',
    'recmomend_detail': '推荐明细',
}
res_dict = {
    'status': True,
    'message': None,
    'data': None,
}
city_obj = models.RegionalManagement.objects.filter(Q(r_code__isnull=False)).all()


@login_required
def index(request):
    default_city = request.session.get('default_city')
    user_dict = user_info(request)
    counts_dict = order_counts(user_dict['phone'])
    return render(request, 'user/user_index.html', {'title': title['index'],
                                                    'user_info': user_dict,
                                                    'counts_dict': counts_dict,
                                                    'city_obj': city_obj,
                                                    'default_city': default_city, })


@login_required
def order(request):
    default_city = request.session.get('default_city')
    user_dict = user_info(request)
    if user_dict.get('phone'):
        order_obj = models.Orders.objects.filter(phone=user_dict['phone']).order_by('-ctime').all()
        counts_dict = order_counts(user_dict['phone'])
        return render(request, 'user/order.html', {'order_obj': order_obj,
                                                   'user_info': user_dict,
                                                   'counts_dict': counts_dict,
                                                   'city_obj': city_obj,
                                                   'title': title['order'],
                                                   'id': 0,
                                                   'default_city': default_city,
                                                   })
    else:
        return redirect('login')


@login_required
def order_topay(request, nid):
    if request.method == 'GET':
        phone = request.session.get('user_info')['phone']
        order_dict = models.Orders.objects.filter(id=nid, phone=phone).all()
        if order_dict:
            pay_dict = models.OrderPayment.objects.filter(order_code=list(order_dict)[0].order_code).first()
            if pay_dict:
                if pay_dict.status == 1:
                    for line in order_dict:
                        line.order_state = 1
                        line.save()
                else:
                    return redirect('shopping_pay', pay_dict.id)
    return redirect('user_order')


@login_required
def order_query(request, id):
    default_city = request.session.get('default_city')
    user_dict = user_info(request)
    phone = user_dict['phone']
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
    return render(request, 'user/order.html', {'title': title['order'],
                                               'user_info': user_dict,
                                               'order_obj': order_obj,
                                               'counts_dict': counts_dict,
                                               'city_obj': city_obj,
                                               'id': id,
                                               'default_city': default_city,
                                               })


@login_required
def order_process_query(req, id):
    if req.method == 'GET':
        order_obj = models.Process.objects.filter(order_id=id).values('step_name', 'date').order_by('date')
        if order_obj:
            res_dict['status'] = True
            res_dict['data'] = list(order_obj)
            res_dict['message'] = None
        else:
            res_dict['status'] = False
            res_dict['message'] = '暂无数据'

    return JsonResponse(res_dict, encoder=DateTypeJSONEncoder)


@login_required
def cancelorders(request):
    nid = request.GET.get('id')
    order_obj = models.Orders.objects.filter(id=nid).first()
    if order_obj:
        models.OrderPayment.objects.filter(order_code=order_obj.order_code).update(status=3)
        models.Orders.objects.filter(order_code=order_obj.order_code).update(order_state=3)
        res_dict['status'] = True
    else:
        res_dict['status'] = False
        res_dict['message'] = '非法操作'
    return JsonResponse(res_dict)


@login_required
def info(request):
    default_city = request.session.get('default_city')
    form = EditProfileForm(request.POST or None)
    phone = request.session.get('user_info')['phone']
    user_dict = models.Users.objects.filter(phone=phone).values('phone', 'email',
                                                                'name', 'province',
                                                                'city', 'area', 'address').first()
    shop_list = request.session.get('shop_list')
    if not shop_list:
        user_dict['shop_number'] = 0
    else:
        user_dict['shop_number'] = len(shop_list)
    if request.method == 'POST':
        if form.is_valid():
            email = request.POST.get('email')
            name = request.POST.get('name')
            address = request.POST.get('address')
            know = request.POST.get('know')
            models.Users.objects.filter(phone=phone).update(email=email, name=name, address=address, know=know)
            res_dict['message'] = '修改成功'
        else:
            res_dict['status'] = False
            res_dict['message'] = list(form.errors.values())[0][0]

        return JsonResponse(res_dict)

    return render(request, 'user/profile.html', {'title': title['info'],
                                                 'form': form,
                                                 'user_info': user_dict,
                                                 'default_city': default_city,
                                                 'city_obj': city_obj,
                                                 })


@login_required
def edit_phone(request):
    default_city = request.session.get('default_city')
    form = EditPhoneForm(request.POST or None)
    user_dict = user_info(request)
    phone = user_dict['phone']

    if request.method == 'POST':
        if form.is_valid():
            new_phone = request.POST.get('phone')
            password = request.POST.get('password')
            verify_code = request.POST.get('verify_code')
            verify_info = \
                models.MessagesVerifyCode.objects.filter(m_phone=phone, ).values_list('m_verifycode',
                                                                                      'm_send_date').order_by(
                    '-m_send_date').first()
            user_obj = models.Users.objects.filter(phone=phone, password=password).first()
            if user_obj and verify_info:
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

    return render(request, 'user/edit_phone.html', {'title': title['edit_phone'],
                                                    'default_city': default_city,
                                                    'user_info': user_dict,
                                                    'city_obj': city_obj, })


@login_required
def edit_pwd(request):
    default_city = request.session.get('default_city')
    user_dict = user_info(request)
    form = EditPwdForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            phone = user_dict['phone']
            password = request.POST.get('password')
            models.Users.objects.filter(phone=phone).update(password=password)
            res_dict['message'] = '请使用新密码重新登录'
        else:

            res_dict['status'] = False
            res_dict['message'] = list(form.errors.values())[0][0]

        return JsonResponse(res_dict)

    return render(request, 'user/edit_password.html', {'title': title['edit_pwd'],
                                                       'default_city': default_city,
                                                       'user_info': user_dict,
                                                       'city_obj': city_obj, })


@login_required
def message_unread(req):
    pass


@login_required
def message_read(req):
    pass


@login_required
def coupon(request):
    default_city = request.session.get('default_city')
    user_dict = user_info(request)
    user_dict['coupon_link'] = 1
    coupon_obj = models.Coupon2User.objects.filter(user_id=user_dict['id'], used=0)

    context = {'default_city': default_city,
               'title': title['coupon'],
               'user_info': user_dict,
               'coupon_obj': coupon_obj,
               'city_obj': city_obj}
    return render(request, 'user/coupon_index.html', context)


@login_required
def coupon_used(request):
    default_city = request.session.get('default_city')
    user_dict = user_info(request)
    user_dict['coupon_link'] = 2
    coupon_obj = models.Coupon2User.objects.filter(user_id=user_dict['id'], used=1)
    context = {'default_city': default_city,
               'title': title['coupon'],
               'user_info': user_dict,
               'coupon_obj': coupon_obj, }
    return render(request, 'user/coupon_index.html', context)


@login_required
def coupon_expired(request):
    default_city = request.session.get('default_city')
    user_dict = user_info(request)
    user_dict['coupon_link'] = 3
    coupon_obj = models.Coupon2User.objects.filter(user_id=user_dict['id'], used=0, coupon__isExpired=0)
    context = {'default_city': default_city,
               'title': title['coupon'],
               'user_info': user_dict,
               'coupon_obj': coupon_obj, }
    return render(request, 'user/coupon_index.html', context)


@login_required
def recmomend(request):
    default_city = request.session.get('default_city')
    error = ''
    user_dict = user_info(request)
    form_obj = UserRecommendForm(request.POST or None)

    if request.method == 'POST':
        if form_obj.is_valid():
            data = form_obj.cleaned_data
            user_obj = models.Users.objects.filter(phone=data['phone']).filter()
            if not user_obj:
                data['type'] = 1
                data['business'] = str(request.POST.getlist('business'))
                data['recommend_id'] = user_dict['id']
                models.UserRecommend.objects.create(**data)
                return redirect('user_index')
            else:
                error = '非常抱歉，该手机号码已注册'
        else:
            error = list(form_obj.errors.values())[0][0]

    context = {'default_city': default_city,
               'user_info': user_dict,
               'title': title['recmomend'],
               'error': error,
               'form_obj': form_obj,
               'city_obj': city_obj, }

    return render(request, 'user/recommend.html', context)


@login_required
def recmomend_count(request):
    return render(request, 'user/recommend_count.html')


@login_required
def recmomend_detail(request):
    default_city = request.session.get('default_city')
    user_dict = user_info(request)
    recommend_obj = models.UserRecommend.objects.filter(recommend_id=user_dict['id'])
    context = {'default_city': default_city,
               'user_dict': user_dict,
               'title': title['recmomend_detail'],
               'recommend_obj': recommend_obj,
               }
    return render(request, 'user/recommend_detail.html', context)


def send_verify_code(req):
    res_dict = {'status': True, 'message': None, 'data': None, }
    if req.method == 'GET':
        phone = req.GET.get('phone')
        type = req.GET.get('type')
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
                user_obj = models.Users.objects.filter(phone=phone).first()
                if user_obj:
                    res_dict['status'] = False
                    res_dict['message'] = '该手机号码已注册'

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
        if not ret:
            res_dict['status'] = False
            res_dict['message'] = '服务器生成验证码失败，请重新尝试'
        return JsonResponse(res_dict)
