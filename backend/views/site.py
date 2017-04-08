from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from backend.forms.forms_site import BxsilderForm, BxsilderEditForm
from backend import forms
from reposition import model_query, model_add, model_update, modal_del
import uuid
import os
from sdy.settings import BASE_DIR
from reposition import models

result_dict = {'status': True, 'message': None, 'data': None}


def site_manage(req):
    title = '站点配置'
    return render(req,
                  'sites/site.html', {
                      'title': title,
                  })


def bxslider(req):
    title = '站点配置-首页轮播图'
    form = BxsilderForm()
    obj = model_query.query_all(models.Bxslider)
    return render(req, 'sites/bxslider.html', {
        'title': title,
        'form': form,
        'obj': obj,
    })


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
            data['size'] = img.size
            data['name'] = name
            data['img'] = file_path
            res = model_add.Add_info(models.Bxslider, data)

            if res == True:
                result_dict['message'] = '图片上传成功'
                return JsonResponse(result_dict)
            else:
                result_dict['message'] = res

        result_dict['message'] = list(obj.errors.values())[0][0]
    result_dict['status'] = False
    return JsonResponse(result_dict)


def bxslider_edit(req):
    if req.method == 'POST':
        obj = BxsilderEditForm(req.POST, req.FILES)
        data = model_update.update_info(models.Bxslider, req.POST.get('nid'))

        if obj.is_valid() and data:
            try:
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
                data.weight = req.POST.get('weight')
                data.save()
                result_dict['message'] = '信息修改成功'
                return JsonResponse(result_dict)
            except Exception as e:
                pass
        else:
            result_dict['message'] = list(obj.errors.values())[0][0]
    else:
        result_dict['message'] = '非法操作'

    result_dict['status'] = False
    return JsonResponse(result_dict)


def bxslider_del(req, id):
    res = modal_del.query_del(models.Bxslider, id)
    if res == True:
        return HttpResponse('成功')
    return HttpResponse(res)
