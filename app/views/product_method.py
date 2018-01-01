from reposition import models


def cart_info(request):
    p_id = request.GET.get('pid')
    pp_id = request.GET.get('ppid')
    # 套餐
    if pp_id:
        package_obj = models.Package.objects.filter(id=pp_id).first()
    else:
        package_obj = None
    # print('shop_list',shop_list)
    shop_list = request.session.get('shop_list')
    if not shop_list:
        shop_list = {'info': {}, 'coupon': {'price': 0, 'coupon_id': []}, 'product': []}

    # 产品
    if p_id:
        product_dict = models.Products.objects.filter(id=p_id).values('p_name', 'p_business_id', 'p_price',
                                                                      'p_category__name', 'area__name',
                                                                      'city__name').first()
    else:
        product_dict = {}

    if product_dict:
        product_dict.update({'product_id': p_id})

    shop_list = shop_list_append(product_dict, shop_list, package_obj)

    return shop_list


def productPackage_info(request):
    data_list = request.POST.getlist('nid')
    shop_list = request.session.get('shop_list')
    if not shop_list:
        shop_list = {'info': {}, 'coupon': {'price': 0, 'coupon_id': []}, 'product': []}
    # print('data_list',type(data_list[0]))
    for data in eval(data_list[0]):
        # print('data', type(data), data)
        p_id = data['nid']
        # 产品
        if p_id:
            product_dict = models.Products.objects.filter(id=p_id).values('p_name', 'p_business_id', 'p_price',
                                                                          'p_category__name', 'area__name',
                                                                          'city__name').first()
        else:
            product_dict = {}

        if product_dict:
            product_dict.update({'product_id': p_id})
        shop_list = shop_list_append(product_dict, shop_list)

    return shop_list


def shop_list_append(product_dict, shop_list, package_obj=None):
    """
    把产品或者套餐放入购物车中
    :param package_obj: 套餐对象
    :param product_dict: 产品信息
    :param shop_list: 购物车
    :return:
    """
    # shop_list表的样子
    """
    {
    info:{},
    coupon:[],
    product:[{'p_id': 14, 'basic': {'type': '0', 'info': {
        'pid': 14, 'number': 1, 'detail': {
            'p_business': 1, 'area__name': '顺德区', 'city__name': '佛山市', 'p_category__name': '有限公司注册',
            'p_name': '111', 'p_price': 111.1}}}}

     {'pp_id': 1, 'basic': {'type' = 1, {'info': {'ppid': 11,
                                                  'name': 123123
                                                  'number': 1,
                                                  'cprice': 222,
                                                  'detail': [{'p_business': 1, 'area__name': '顺德区',
                                                              'city__name': '佛山市', 'p_category__name': '有限公司注册',
                                                              'p_name': '111', 'p_price': 111.1}, ]}}}}
    ]
    }
    """
    if package_obj:
        # 判断套餐是否已经放入购物车中 返回结果为True 代表没有
        status = get_status(shop_list, 'pp_id', package_obj.id)
        if status:
            shop_list = shop_list_package_append(product_dict, package_obj, shop_list)

    elif product_dict:
        status = get_status(shop_list, 'p_id', product_dict['product_id'])
        # 产品
        if status:
            product_info_dict = {'p_id': product_dict['product_id'],
                                 'basic': {'type': 0, 'info': {'number': 1,
                                                               'pid': product_dict['product_id'],
                                                               'detail': [product_dict, ]}}}
            shop_list['product'].append(product_info_dict)
    return shop_list


def shop_list_package_append(product_dict, package_obj, shop_list):
    """
    把套餐放入购物车
    :param product_dict: 产品信息的字典
    :param package_obj: 套餐对象
    :param shop_list: 购物列表
    :return:
    """
    packages2products_obj = models.Package2Product.objects.filter(package_id=package_obj.id).all()
    product_list = []
    if packages2products_obj:
        if product_list:
            product_list.append(product_dict)
        for packages2product_obj in packages2products_obj:

            if not product_dict or str(packages2product_obj.product.id) != product_dict['product_id']:
                product_info_dict = {'product_id': packages2product_obj.product.id,
                                     'p_name': packages2product_obj.product.p_name,
                                     'p_price': packages2product_obj.product.p_price,
                                     'p_business_id': packages2product_obj.product.p_business_id,
                                     'area__name': packages2product_obj.product.area.name,
                                     'city__name': packages2product_obj.product.city.name,
                                     'p_category__name': packages2product_obj.product.p_category.name}
                product_list.append(product_info_dict)

    info_dict = {'pp_id': package_obj.id, 'basic': {'type': 1, 'info': {'ppid': package_obj.id,
                                                                        'name': package_obj.name,
                                                                        'number': 1,
                                                                        'cprice': package_obj.cprice,
                                                                        'detail': product_list}
                                                    }
                 }
    shop_list['product'].append(info_dict)
    return shop_list


def get_status(shop_list, type, id):
    """
    判断放入购物车的商品是否已存在购物车中
    :param shop_list:
    :param type: pid 代表产品 ppid 代表套餐
    :param id:
    :return:True 代表没有
    """
    status = True
    for line in shop_list['product']:
        # print('line.get(type)', line.get(type))
        if id == line.get(type):
            status = False
            break
    return status
