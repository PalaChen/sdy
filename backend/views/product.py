from django.shortcuts import render, redirect, HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from reposition import models, modal_del
from backend.forms.product import ProductForm, ImageForm, ProCategoryForm, ProBusinessForm, \
    ProServiceForm, PackageAdd, PackageBind, ConponForm
from utils.upload_image import save_image
from utils.pager import paginator
from utils.upload_image import ckedit_upload_image
from utils.login_admin import login_required, permission
from cxmadmin import base
from django.db.models import Q

# product方法
from . import product_method

res_dict = {'status': 200, 'data': None, 'message': None}
title_dict = {
    'p_category': '分类管理',
    'p_category_add': '分类管理',
    'p_category_edit': '分类修改 ',
    'p_category_del': '分类删除',
    'p_service': '服务管理',
    'p_service_add': '服务添加',
    'p_service_edit': '服务修改',
    'p_service_del': '服务删除',
    'p_business': '业务管理',
    'p_business_add': '业务添加',
    'p_business_edit': '业务修改',
    'p_business_del': '业务删除',
    'product': '我的产品',
    'product_add': '产品添加',
    'product_edit': '产品修改',
    'product_del': '产品删除',
    'package': '优惠套餐',
    'package_add': '套餐添加',
    'package_edit': '套餐修改',
    'package_bind': '产品绑定套餐',
    'coupon': '优惠卷管理',
    'coupon_add': '优惠卷添加',
    'coupon_edit': '优惠卷修改',
}


# 产品分类管理
# @login_required
# @permission
def p_category(req, *args, **kwargs):
    action_list = kwargs.get('action_list')
    menu_string = kwargs.get('menu_string')
    form = ProCategoryForm()
    category_obj = models.ProductCategory.objects.order_by('root_id', 'parent_id', '-sort')
    cate_r_list = []
    cate_p_list = []
    cate_c_list = []
    for row in category_obj:
        if row.root_id == 9999 and row.parent_id != 0:
            cate_c_list.append(row)
        elif row.root_id == 0:
            cate_r_list.append(row)
        else:
            cate_p_list.append(row)
    return render(req, 'product/p_category.html', {'form': form,
                                                   'title': title_dict['p_category'],
                                                   'cate_r_list': cate_r_list,
                                                   'cate_p_list': cate_p_list,
                                                   'cate_c_list': cate_c_list,
                                                   'menu_string': menu_string,
                                                   })


# 产品分类添加
@login_required
@permission
def p_category_add(req, *args, **kwargs):
    if req.method == 'POST':
        form = ProCategoryForm(req.POST)

        if form.is_valid():
            data = form.cleaned_data

            data['employee_id'] = req.session.get('user_info')['employee_id']
            id = data['root_id']
            category_obj = models.ProductCategory.objects.filter(id=id).values('id', 'root_id',
                                                                               'parent_id').first()
            # 判断category_obj是否为空
            if category_obj:
                if category_obj['root_id'] == 0 and category_obj['parent_id'] == 0:
                    data['root_id'] = id
                else:
                    data['root_id'] = 9999
                    data['parent_id'] = id
            else:
                data['root_id'] = 0
            try:
                models.ProductCategory.objects.create(**data)
                res_dict['message'] = '分类添加成功'
            except Exception as e:
                res_dict['message'] = '非法数据操作'
                res_dict['status'] = 500
        else:
            error = list(form.errors.values())[0][0]
            res_dict['message'] = error
            res_dict['status'] = 400
    # print(form.errors)
    return JsonResponse(res_dict)


# 产品分类修改
@login_required
@permission
def p_category_edit(req, *args, **kwargs):
    if req.method == 'POST':
        form = ProCategoryForm(req.POST)
        if form.is_valid():
            data = form.cleaned_data
            nid = req.POST.get('nid')
            category_obj = models.ProductCategory.objects.filter(id=nid).first()
            if category_obj:
                data['employee_id'] = req.session.get('user_info')['employee_id']
                id = data['root_id']
                if 0 < category_obj.root_id < 9999:
                    data['root_id'] = id
                elif category_obj.root_id == 0:
                    data['root_id'] = 0
                    data['parent_id'] = id
                else:
                    data['root_id'] = 9999
                    data['parent_id'] = id
                    # try:

                models.ProductCategory.objects.filter(id=nid).update(**data)
                res_dict['message'] = '分类修改成功'
                # except Exception as e:
                #     res_dict['message'] = '非法数据操作'
                #     res_dict['status'] = 500
        else:
            error = list(form.errors.values())[0][0]
            res_dict['message'] = error
            res_dict['status'] = 400
    return JsonResponse(res_dict)


# 产品分类删除
@login_required
@permission
def p_category_del(req, id, *args, **kwargs):
    res = modal_del.query_del(req, models.ProductCategory, id)
    return HttpResponse(res)


# 服务管理
@login_required
@permission
def p_service(req, *args, **kwargs):
    action_list = kwargs.get('action_list')
    menu_string = kwargs.get('menu_string')
    service_obj = models.ProductService.objects.all().order_by('-ctime')
    posts = paginator(req, service_obj)
    return render(req, 'product/p_service.html', {'title': title_dict['p_service'],
                                                  'menu_string': menu_string,
                                                  'posts': posts})


# 服务添加
@login_required
@permission
def p_service_add(req, *args, **kwargs):
    menu_string = kwargs.get('menu_string')
    form = ProServiceForm(req.POST or None)
    select_obj = models.ProductService.objects.filter(Q(root_id=None)).values('id', 'name').all()
    if req.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data
            data['employee_id'] = req.session.get('user_info')['employee_id']
            models.ProductService.objects.create(**data)
            return redirect('p_service')

    return render(req, 'product/p_service_add.html', {'form': form,
                                                      'select_obj': select_obj,
                                                      'menu_string': menu_string,
                                                      'title': title_dict['p_service_add'],})


# 服务修改
@login_required
@permission
def p_service_edit(req, id, *args, **kwargs):
    menu_string = kwargs.get('menu_string')
    service_obj = models.ProductService.objects.filter(id=id).first()
    select_obj = models.ProductService.objects.filter(Q(root_id=None)).values('id', 'name').all()
    form = ProServiceForm()
    if req.method == 'POST':
        form = ProServiceForm(req.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['employee_id'] = req.session.get('user_info')['employee_id']
            models.ProductService.objects.filter(id=id).update(**data)
            return redirect('p_service')
            #
    return render(req, 'product/p_service_edit.html', {'title': title_dict['p_service_edit'],
                                                       'service_obj': service_obj,
                                                       'select_obj': select_obj,
                                                       'menu_string': menu_string,
                                                       'form': form})


# 服务删除
@login_required
@permission
def p_service_del(req, id, *args, **kwargs):
    menu_string = kwargs.get('menu_string')
    pass


# 业务管理
@login_required
@permission
def p_business(req, *args, **kwargs):
    action_list = kwargs.get('action_list')
    menu_string = kwargs.get('menu_string')
    business_obj = models.ProcessName.objects.all()
    posts = paginator(req, business_obj)
    processsep_obj = models.ProcessStep.objects.all().order_by('p_name_id', 'number')
    return render(req, 'product/p_business.html', {'menu_string': menu_string,
                                                   'title': title_dict['p_business'],
                                                   'posts': posts,
                                                   'processsep_obj': processsep_obj})


# 业务添加
@login_required
@permission
def p_business_add(req, *args, **kwargs):
    menu_string = kwargs.get('menu_string')
    form = ProBusinessForm(req.POST or None)
    error = None
    if req.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            user_info = req.session.get('user_info')
            name_obj = models.ProcessName.objects.filter(name=name).first()
            if not name_obj:
                name_obj = models.ProcessName.objects.create(name=name, employee_id=user_info['employee_id'])
                step_number = req.POST.getlist('step_number')
                step_name = req.POST.getlist('step_name')
                for step_number, step_name in zip(step_number, step_name):
                    data = {'employee_id': user_info['employee_id'],
                            'p_name_id': name_obj.id, 'process_name': name,}
                    data.update({'number': step_number, 'name': step_name})
                    models.ProcessStep.objects.create(**data)
                return redirect('p_business')
        else:
            error = list(form.errors.values())[0][0]

    return render(req, 'product/p_business_add.html', {'title': title_dict['p_business_add'],
                                                       'form': form,
                                                       'menu_string': menu_string,
                                                       'error': error})


# 业务修改
@login_required
@permission
def p_business_edit(req, id, *args, **kwargs):
    menu_string = kwargs.get('menu_string')
    form = ProBusinessForm(req.POST or None)
    error = None
    process_obj = models.ProcessStep.objects.filter(p_name_id=id).values('id', 'number', 'process_name', 'name',
                                                                         'p_name_id').all()
    step_exist_list = []
    for line in process_obj:
        step_exist_list.append(line['number'])
    if req.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            employee_id = req.session.get('user_info')['employee_id']

            name_obj = models.ProcessName.objects.filter(id=id).first()
            if name_obj:
                name_obj.name = name
                name_obj.save()
            step_number = req.POST.getlist('step_number')
            step_name = req.POST.getlist('step_name')

            data_dict = {}
            for step_number, step_name, in zip(step_number, step_name, ):
                data_dict.update(
                    {int(step_number): {'employee_id': employee_id, 'p_name_id': id, 'process_name': name}})
                data_dict[int(step_number)].update({'number': step_number, 'name': step_name})
            step_new_list = list(data_dict.keys())

            # 交集
            intersection = set(step_exist_list) & set(step_new_list)
            if intersection:
                for i in intersection:
                    for line in process_obj:
                        if i == line['number']:
                            if data_dict[i]['name'] == line['name']:
                                pass
                            else:
                                models.ProcessStep.objects.filter(p_name_id=id, number=i).update(**data_dict[i])
            # 左交集
            left_intersection = set(step_exist_list) - set(step_new_list)
            if left_intersection:
                for i in left_intersection:
                    models.ProcessStep.objects.filter(p_name_id=id, number=i).delete()

            right_intersection = set(step_new_list) - set(step_exist_list)
            # 右交集
            if right_intersection:
                for i in right_intersection:
                    models.ProcessStep.objects.create(**data_dict[i])

            return redirect('p_business')
        else:
            error = list(form.errors.values())[0][0]
    return render(req, 'product/p_business_edit.html', {'title': title_dict['p_business_edit'],
                                                        'form': form,
                                                        'error': error,
                                                        'menu_string': menu_string,
                                                        'process_obj': process_obj})


# 业务删除
@login_required
@permission
def p_business_del(request, id, *args, **kwargs):
    if request.method == 'GET':
        models.ProcessName.objects.filter(id=id).delete()
        models.ProcessStep.objects.filter(p_name_id=id).all().delete()
        return HttpResponse('成功')
    return HttpResponse('失败')


from django.db import connection


@login_required
@permission
def product(req, *args, **kwargs):
    action_list = kwargs.get('action_list')
    menu_string = kwargs.get('menu_string')
    product_obj = models.Products.objects.all().order_by('-p_ctime')
    posts = paginator(req, product_obj)

    return render(req, 'product/product.html', {'title': title_dict['product'],
                                                'menu_string': menu_string,
                                                'posts': posts,
                                                })


# 添加产品
@login_required
@permission
def product_add(req, *args, **kwargs):
    menu_string = kwargs.get('menu_string')
    form = ProductForm(req.POST or None)
    business_obj, city_obj, service_list = product_general()
    error = ''
    if req.method == 'POST':
        # 保存信息
        if form.is_valid():
            # p_service_id = form.cleaned_data.get('p_service_id')
            # product_obj = models.Products.objects.filter(p_service_id=p_service_id).first()
            # if not product_obj:
            data = form.cleaned_data
            id = data.pop('p_t_imgae')
            data['p_employee_id'] = req.session.get('user_info')['employee_id']
            area_code = data.pop('area_code')
            city_code = data.pop('city_code')
            area_obj = get_object_or_404(models.RegionalManagement, code=area_code)
            city_obj = get_object_or_404(models.RegionalManagement, code=city_code)

            data['area_id'] = area_obj.id
            data['city_id'] = city_obj.id
            product_obj = models.Products.objects.create(**data)
            models.ProductTImage.objects.filter(id=id).update(ul_product=product_obj)
            return redirect('product_all')
            # else:
            #     error = '一个产品同一个地区只能对应一个服务,该服务已绑定产品，请选择其他服务'
        else:
            error = list(form.errors.values())[0][0]
    return render(req, 'product/product_add.html', {'form': form,
                                                    'title': title_dict['product_add'],
                                                    'business_obj': business_obj,
                                                    'service_list': service_list,
                                                    'city_obj': city_obj,
                                                    'error': error,
                                                    'menu_string': menu_string,
                                                    })


def get_city_info(request):
    if request.method == 'GET':
        city_obj = models.RegionalManagement.objects.all().values_list('code', 'name').order_by('city_id')
        city_dict = {}
        for code, name in city_obj:
            city_dict.update({code: name})
        return JsonResponse(city_dict)


# 产品头图片上传
@login_required
def product_image_upload(request):
    res_dict = {'status': True, 'data': None, 'message': None}
    if request.method == 'POST':
        files = ImageForm(request.POST, request.FILES)
        if files.is_valid():
            img = request.FILES.get('img')
            data = save_image(img)
            if data:
                data['ul_employee_id'] = request.session.get('user_info')['employee_id']
                image_obj = models.ProductTImage.objects.create(**data)
                res_dict['data'] = data['ul_url']
                res_dict['message'] = image_obj.id
                return JsonResponse(res_dict)
    res_dict['status'] = False
    return JsonResponse(res_dict)


# 产品内容图片
@login_required
def product_ck_image(req):
    res_dict = ckedit_upload_image(req, 'product')
    return JsonResponse(res_dict)


# 产品修改
@login_required
@permission
def product_edit(req, id, *args, **kwargs):
    menu_string = kwargs.get('menu_string')
    product_obj = models.Products.objects.filter(id=id).first()

    product_image_obj = models.ProductTImage.objects.filter(ul_product_id=product_obj.id).first()
    # print(product_image_obj)
    # 把产品数据处理为字典放入form
    product_dict = {'p_name': product_obj.p_name, 'p_category_id': product_obj.p_category_id,
                    'p_service_id': product_obj.p_service_id, 'p_business_id': product_obj.p_business_id,
                    'city_code': product_obj.city.code, 'area_code': product_obj.area.code,
                    'p_top': product_obj.p_top, 'p_putaway': product_obj.p_putaway,
                    'p_price': product_obj.p_price, 'p_market_price': product_obj.p_market_price,
                    'p_seo_keyword': product_obj.p_seo_keyword, 'p_seo_description': product_obj.p_seo_description,
                    'p_details': product_obj.p_details,}
    business_obj, city_obj, service_list = product_general()
    form = ProductForm(data=product_dict, )
    if req.method == 'GET':
        # 错误信息为空，因为传入输入数据时form会进行数据验证，而p_t_imgae的值无法直接拿到
        form._errors = ''

    if req.method == 'POST':
        form = ProductForm(req.POST)
        if form.is_valid():
            data = form.cleaned_data

            image_id = data.pop('p_t_imgae')
            area_code = data.pop('area_code')
            city_code = data.pop('city_code')

            # 判断用户是否更改城市
            if city_code != product_obj.city.code:
                city_obj = get_object_or_404(models.RegionalManagement, code=city_code)
                data['city_id'] = city_obj.id

            # 判断用户是否更改地区
            if area_code != product_obj.area.code:
                area_obj = get_object_or_404(models.RegionalManagement, code=area_code)
                data['area_id'] = area_obj.id
            # 判断用户是否更改图片

            if image_id:
                product_image_obj.ul_product_id = None
                product_image_obj.save()
                models.ProductTImage.objects.filter(id=image_id).update(ul_product_id=id)

            data['p_employee_id'] = req.session.get('user_info')['employee_id']
            models.Products.objects.filter(id=id).update(**data)
            return redirect('product_all')

    return render(req, 'product/product_edit.html', {'title': title_dict['product_edit'],
                                                     'form': form,
                                                     'business_obj': business_obj,
                                                     'service_list': service_list,
                                                     'city_obj': city_obj,
                                                     'menu_string': menu_string,
                                                     'product_obj': product_obj})


# 产品删除
@login_required
@permission
def product_del(req, id, *args, **kwargs):
    res = modal_del.query_del(req, models.Products, id)
    return HttpResponse(res)


# 添加/修改产品调用的通用信息
def product_general():
    business_obj = models.ProcessName.objects.values('id', 'name').all()
    service_obj = models.ProductService.objects.values('id', 'name', 'root_id').order_by('root_id').all()
    city_obj = models.RegionalManagement.objects.values('id', 'name').all()
    service_list = []

    for line in service_obj:
        if not line['root_id']:
            service_list.append((line, []))
        else:
            for index, l in enumerate(service_list):
                if line['root_id'] == l[0]['id']:
                    service_list[index][1].append(line)
    return business_obj, city_obj, service_list


@login_required
def attribute(req):
    pass


@login_required
@permission
def package(request, *args, **kwargs):
    common_info = {}
    common_info['menu_string'] = kwargs.get('menu_string')
    common_info['title'] = title_dict['package']
    common_info['filter_dict'] = {'status': 1}
    common_info['add_url'] = 'package_city'
    common_info['edit_url'] = 'package_edit'
    common_info['html_url'] = 'product/packages.html'
    return base.table_obj_list(request, 'reposition', 'package', common_info)


@login_required
def package_city(request, *args, **kwargs):
    menu_string = kwargs.get('menu_string')
    title = title_dict['package_add']
    if request.method == 'POST':
        area_code = request.POST.get('area_code')
        area_obj = models.RegionalManagement.objects.filter(code=area_code).first()
        from django.urls import reverse
        url = reverse('package_add')
        return redirect(url + '?area_id=' + str(area_obj.id))
        # return package_add(request, area_obj.id)

    return render(request, 'product/package_city.html', {'title': title,
                                                         'menu_string': menu_string})


@login_required
@permission
def package_add(request, *args, **kwargs):
    error = ''
    menu_string = kwargs.get('menu_string')
    title = title_dict['package_add']
    form_obj = PackageAdd(request.POST or None)

    # area_id = request.GET.get('area_id')
    if request.method == 'POST':
        product_list = request.POST.getlist('product_id')
        if product_list:
            if form_obj.is_valid():
                data_dict = form_obj.cleaned_data
                package_name = request.POST.get('name')
                is_exit = models.Package.objects.filter(name=package_name).first()
                if not is_exit:
                    data_dict['employee_id'] = request.session.get('user_info')['employee_id']
                    package_obj = models.Package.objects.create(**data_dict)
                    for product_id in product_list:
                        models.Package2Product.objects.create(product_id=product_id, package=package_obj)
                    return redirect('package')
                else:
                    error = '套餐名已存在，请重新输入'
            else:
                error = list(form_obj.errors.values())[0][0]
        else:
            error = '套餐中必须要选择对应的商品,请选择该地区对应的商品，否则套餐无法创建成功'

    # 获取地区
    area_id = request.GET.get('area_id')
    if not area_id:
        area_id = request.POST.get('area_id')
        if not area_id:
            return redirect('package_city')
    product_obj = models.Products.objects.filter(p_putaway=1, area_id=area_id).all()
    return render(request, 'product/package_add.html', {'product_obj': product_obj,
                                                        'menu_string': menu_string,
                                                        'title': title,
                                                        'area_id': area_id,
                                                        'error': error,
                                                        'form_obj': form_obj})


@login_required
@permission
def package_edit(request, id, *args, **kwargs):
    form_obj = PackageAdd(request.POST or None)
    menu_string = kwargs.get('menu_string')
    title = title_dict['package_edit']
    # 套餐
    package_obj = models.Package.objects.filter(id=id).first()
    # 套餐中包含的产品
    package2product_obj = models.Package2Product.objects.filter(package=package_obj)
    product_obj = models.Products.objects.filter(p_putaway=1, area_id=package_obj.area_id).all()
    if request.method == 'POST':
        if form_obj.is_valid():
            data_dict = form_obj.cleaned_data
            data_dict['employee_id'] = request.session.get('user_info')['employee_id']
            package_obj = models.Package.objects.filter(id=id).update(**data_dict)
            product_list = request.POST.getlist('product_id')
            # 处理修改后套餐中商品是否存在
            product_method.package_edit_update(product_list, id)
            return redirect('package')

    return render(request, 'product/package_edit.html', {'menu_string': menu_string,
                                                         'form_obj': form_obj,
                                                         'title': title,
                                                         'package_obj': package_obj,
                                                         'package2product_obj': package2product_obj,
                                                         'product_obj': product_obj,})


def package_del(request, *args, **kwargs):
    pass


# @login_required
def package_bind(request, package_id, *args, **kwargs):
    form_obj = PackageBind(request.POST or None)
    title = title_dict['package_edit']

    if request.method == 'POST':
        error = ''
        if form_obj.is_valid():
            product_list = request.POST.getlist('product_id')
            package_id = request.POST.get('package_id')
            product_method.product2package_edit_update(product_list, package_id)
            return redirect('package')
        else:
            error = list(form_obj.errors.values())[0][0]

    package_obj = models.Package.objects.filter(id=package_id).first()
    product2package_obj = models.Product2Package.objects.filter(package_id=package_obj)
    products_obj = models.Products.objects.filter(area=package_obj.area).all()
    return render(request, 'product/package_bind.html', {'products_obj': products_obj,
                                                         'title': title,
                                                         'product2package_obj': product2package_obj,
                                                         'package_obj': package_obj})


@login_required
@permission
def coupon(request, *args, **kwargs):
    common_info = {}
    common_info['menu_string'] = kwargs.get('menu_string')
    common_info['title'] = title_dict['coupon']
    common_info['add_url'] = 'coupon_add'
    common_info['edit_url'] = 'package_edit'
    common_info['html_url'] = 'product/packages.html'
    return base.table_obj_list(request, 'reposition', 'coupon', common_info)


def coupon_add(request):
    title = title_dict['coupon_add']
    form_obj = ConponForm(request.POST or None)
    error = ''
    if request.method == 'POST':
        if form_obj.is_valid():
            data_dict = form_obj.cleaned_data
            # print(data_dict)
            data_dict['employee_id'] = request.session.get('user_info')['employee_id']
            models.Coupon.objects.create(**data_dict)
            return redirect('coupon')
        else:
            error = list(form_obj.errors.values())[0][0]
    d = {
        'title': title,
        'form': form_obj,
        'error': error,
    }
    return render(request, 'product/coupon_add.html', d)
