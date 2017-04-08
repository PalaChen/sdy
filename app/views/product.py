from django.shortcuts import render
from reposition import models
from utils.menu import get_cate_dic

cate_dic = get_cate_dic()


def index(req, id):
    product_obj = models.Products.objects.filter(id=id).first()
    service_obj = models.ProductService.objects.filter(category_id=product_obj.p_category_id).all()
    return render(req, 'product/index.html', {'product_obj': product_obj,
                                              'cate_dic': cate_dic,
                                              'service_obj': service_obj})
