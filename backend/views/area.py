from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from utils.login_admin import login_required, permission

from reposition import models
from cxmadmin import base

title_dict = {'area_index': '区域管理'}
result_dict = {'status': 200, 'message': None, 'data': None}


def area_index(request, *arg, **kwargs):
    common_info = {}
    common_info['menu_string'] = kwargs.get('menu_string')
    common_info['title'] = title_dict['area_index']
    common_info['html_url'] = 'area/area_index.html'
    # common_info['html_url'] = 'area/area_index.html'
    return base.table_obj_list(request, 'reposition', 'regionalmanagement', common_info)


def area_citys(requesst):
    if requesst.method == 'GET':
        city_obj = models.China.objects.all().values_list('code', 'name').order_by('id')
        city_dict = {}
        for code, name in city_obj:
            city_dict.update({code: name})
    return JsonResponse(city_dict)


def area_add(request):
    if request.method == 'POST':
        province = request.POST.get('province')
        city = request.POST.get('city')
        area = request.POST.get('area')
        li = [province, city, area]
        for index, i in enumerate(li):
            if i:
                is_exit = models.RegionalManagement.objects.filter(code=i).first()
                if not is_exit:
                    china_obj = models.China.objects.get(code=i)
                    if china_obj:
                        data = {'city': china_obj,
                                'code': china_obj.code,
                                'name': china_obj.name}
                        if index == 0:
                            pass
                        elif index == 1:
                            data['r_code'] = province
                        elif index == 2:
                            data['p_code'] = city
                        models.RegionalManagement.objects.create(**data)
    return JsonResponse(result_dict)
