from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from backend.forms.forms_site import BxsilderForm, BxsilderEditForm, NavForm
from backend import forms
from reposition import model_query, model_add, model_update, modal_del
import uuid
import os
from sdy.settings import BASE_DIR
from reposition import models
from utils.login_admin import login_required, permission
from cxmadmin import base

result_dict = {'status': True, 'message': None, 'data': None}
title_dict = {'nav': '首页导航', 'nav_add': '添加导航', 'nav_edit': '修改导航',
              'nav_del': '删除导航', 'site_manage': '站点配置',
              'product_recommend': '首页产品推荐'}


@login_required
# @permission
def site_manage(req, *args, **kwargs):
    action_list = kwargs.get('action_list')
    menu_string = kwargs.get('menu_string')

    return render(req, 'sites/site.html', {'menu_string': menu_string,
                                           'title': title_dict['site_manage']})


@login_required
# @permission
def bxslider(req, *args, **kwargs):
    title = '站点配置-首页轮播图'
    form = BxsilderForm()
    # menu_string = kwargs.get('menu_string')
    obj = model_query.query_all(models.Bxslider)
    return render(req, 'sites/bxslider.html', {'title': title,
                                               'form': form,
                                               'obj': obj,
                                               # 'menu_string': menu_string
                                               })


@login_required
def bxslider_upload(req):
    if req.method == 'POST':
        obj = BxsilderForm(req.POST, req.FILES)
        if obj.is_valid():
            img = req.FILES.get('img')
            name = str(uuid.uuid4()) + img.name
            file_path = 'static/upload/focus/' + name

            with open(os.path.join(BASE_DIR, file_path), 'wb') as f:
                for line in img.chunks():
                    f.write(line)
            data = {}
            data["status"] = req.POST.get('status')
            data['weight'] = req.POST.get('weight')
            data['url'] = req.POST.get('url')
            data['size'] = img.size
            data['name'] = name
            data['img'] = file_path
            data['employee_id'] = req.session.get('user_info')['employee_id']

            models.Bxslider.objects.create(**data)
            result_dict['message'] = '图片上传成功'
            return JsonResponse(result_dict)
        else:
            result_dict['message'] = list(obj.errors.values())[0][0]
    result_dict['status'] = False
    return JsonResponse(result_dict)


@login_required
def bxslider_edit(req):
    if req.method == 'POST':
        obj = BxsilderEditForm(req.POST, req.FILES)
        data = models.Bxslider.objects.filter(id=req.POST.get('nid')).first()
        if obj.is_valid() and data:
            # try:
            img = req.FILES.get('img')
            if img:
                name = str(uuid.uuid4()) + img.name
                file_path = 'static/upload/focus/' + name
                with open(os.path.join(BASE_DIR, file_path), 'wb') as f:
                    for line in img.chunks():
                        f.write(line)
                data.size = img.size
                data.name = name
                data.img = file_path
            data.status = req.POST.get('status')
            data.url = req.POST.get('url')
            data.save()
            result_dict['message'] = '信息修改成功'
            return JsonResponse(result_dict)
            # except Exception as e:
            #     result_dict['message'] = '非法操作'
        else:
            result_dict['message'] = list(obj.errors.values())[0][0]
    else:
        result_dict['message'] = '非法操作'
    result_dict['status'] = False
    return JsonResponse(result_dict)


@login_required
def bxslider_del(req, id):
    res = modal_del.query_del(req, models.Bxslider, id)
    if res == True:
        return HttpResponse('成功')
    return HttpResponse(res)


@login_required
def nav(req, *args, **kwargs):
    form = NavForm()
    menu_string = kwargs.get('menu_string')
    nav_obj = models.IndexNav.objects.all()
    return render(req, 'sites/index_nav.html', {'title': title_dict['nav'],
                                                'nav_obj': nav_obj,
                                                'form': form,
                                                'menu_string': menu_string,
                                                })


@login_required
def nav_add(req):
    if req.method == 'POST':
        form = NavForm(req.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['employee_id'] = req.session.get('user_info')['employee_id']
            nav_obj = models.IndexNav.objects.filter(name=data['name']).first()
            if not nav_obj:
                models.IndexNav.objects.create(**data)
                result_dict['status'] = 200
                result_dict['message'] = '导航添加成功'
                return JsonResponse(result_dict)
        else:
            # print(form.errors)
            result_dict['message'] = list(form.errors.values())[0][0]
    result_dict['status'] = False
    return JsonResponse(result_dict)


@login_required
def nav_edit(request):
    if request.method == 'POST':
        form = NavForm(request.POST)
        if form.is_valid():
            id = request.POST.get('nid')
            data = form.cleaned_data
            data['employee_id'] = request.session.get('user_info')['employee_id']
            nav_obj = models.IndexNav.objects.filter(id=id).first()
            if nav_obj:
                models.IndexNav.objects.filter(id=id).update(**data)
                result_dict['status'] = 200
                result_dict['message'] = '导航修改成功'
                return JsonResponse(result_dict)
        else:
            # print(form.errors)
            result_dict['message'] = list(form.errors.values())[0][0]
    result_dict['status'] = False
    return JsonResponse(result_dict)


@login_required
def nav_del(request, id):
    res = modal_del.query_del(request, models.IndexNav, id)
    return HttpResponse(res)


@login_required
def product_recommend(request, *arg, **kwargs):
    common_info = {}
    # models.ProcessStep.objects.filter(p_name=)
    common_info['menu_string'] = kwargs.get('menu_string')
    common_info['title'] = title_dict['product_recommend']
    common_info['html_url'] = 'sites/product_recommend.html'
    return base.table_obj_list(request, 'reposition', 'productrecommend', common_info)


def banner(request):
    title = '站点配置-广告图片管理'
    form = BxsilderForm()
    # menu_string = kwargs.get('menu_string')
    obj = model_query.query_all(models.Banner)
    return render(request, 'sites/banner.html', {'title': title,
                                                 'form': form,
                                                 'obj': obj,
                                                 })


@login_required
def banner_upload(request):
    if request.method == 'POST':
        obj = BxsilderForm(request.POST, request.FILES)
        if obj.is_valid():
            img = request.FILES.get('img')
            name = str(uuid.uuid4()) + img.name
            file_path = 'static/upload/focus/' + name

            with open(os.path.join(BASE_DIR, file_path), 'wb') as f:
                for line in img.chunks():
                    f.write(line)
            # print('position',request.POST.get('position'))
            data = {}
            data["status"] = request.POST.get('status')
            data['position'] = request.POST.get('position')
            data['url'] = request.POST.get('url')
            data['size'] = img.size
            data['name'] = name
            data['img'] = file_path
            data['employee_id'] = request.session.get('user_info')['employee_id']

            models.Banner.objects.create(**data)
            result_dict['message'] = '图片上传成功'
            return JsonResponse(result_dict)
        else:
            result_dict['message'] = list(obj.errors.values())[0][0]
    result_dict['status'] = False
    return JsonResponse(result_dict)


@login_required
def banner_edit(req):
    if req.method == 'POST':
        obj = BxsilderEditForm(req.POST, req.FILES)
        data = models.Banner.objects.filter(id=req.POST.get('nid')).first()
        if obj.is_valid() and data:
            # try:
            img = req.FILES.get('img')
            if img:
                name = str(uuid.uuid4()) + img.name
                file_path = 'static/upload/focus/' + name
                with open(os.path.join(BASE_DIR, file_path), 'wb') as f:
                    for line in img.chunks():
                        f.write(line)
                data.size = img.size
                data.name = name
                data.img = file_path
            data.status = req.POST.get('status')
            data.position = req.POST.get('position')
            data.url = req.POST.get('url')
            data.save()
            result_dict['message'] = '信息修改成功'
            return JsonResponse(result_dict)
            # except Exception as e:
            #     result_dict['message'] = '非法操作'
        else:
            result_dict['message'] = list(obj.errors.values())[0][0]
    else:
        result_dict['message'] = '非法操作'
    result_dict['status'] = False
    return JsonResponse(result_dict)


@login_required
def banner_del(req, id):
    res = modal_del.query_del(req, models.Banner, id)
    if res == True:
        return HttpResponse('成功')
    return HttpResponse(res)
