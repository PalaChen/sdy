from django.shortcuts import render, redirect
from django.http import JsonResponse
from reposition import models
from utils.menu import get_cate_dic

cate_dic = get_cate_dic()
result_dict = {'status': 200, 'message': None, 'data': None, 'url': None}
status = {
    200: '正常',
    801: '用户不存在',
}


def index(req, id):
    product_obj = models.Products.objects.filter(id=id).first()
    service_obj = models.ProductService.objects.filter(category_id=product_obj.p_category_id).all()
    nav_list = models.IndexNav.objects.order_by('-weight').values('name', 'url')[0:6]
    return render(req, 'product/index.html', {'product_obj': product_obj,
                                              'cate_dic': cate_dic,
                                              'nav_list': nav_list,
                                              'service_obj': service_obj})


def p_c_index(req, id):
    product_obj = models.Products.objects.filter(p_category_id=id).first()
    service_obj = models.ProductService.objects.filter(category_id=id).all()
    nav_list = models.IndexNav.objects.order_by('-weight').values('name', 'url')[0:6]
    return render(req, 'product/index.html', {'product_obj': product_obj,
                                              'cate_dic': cate_dic,
                                              'nav_list': nav_list,
                                              'service_obj': service_obj})



def buy(request):
    if request.method == 'GET':
        user_info = request.session.get('user_info')
        if user_info:
            id = request.GET.get('pid')

            product_obj = models.Products.objects.filter(id=id).first()
            if product_obj:
                result_dict['url'] = '/cart.html?pid={}'.format(id)
        else:
            result_dict['status'] = 801

        return JsonResponse(result_dict)
