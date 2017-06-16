from reposition import models


def package_edit_update(product_list, package_id):
    """
    处理修改后套餐中商品是否处在Package2Product表中
    :param product_list: 用户选择商品id
    :param package_obj: 套餐id
    :return:
    """
    Package2Product_obj = models.Package2Product.objects.filter(package_id=package_id).values_list(
        'product_id').all()
    package2product_list = []
    for package2product in Package2Product_obj:
        package2product_list.append(str(package2product[0]))
    package2product_list_set = set(package2product_list)
    product_list_set = set(product_list)
    # 交集
    intersection = product_list_set & package2product_list_set
    if intersection:
        pass
    # 左交集
    left_intersection = product_list_set - package2product_list_set
    if left_intersection:
        for product_id in left_intersection:
            models.Package2Product.objects.create(product_id=product_id, package_id=package_id)
    # 有交集
    right_intersection = package2product_list_set - product_list_set
    if right_intersection:
        for product_id in right_intersection:
            models.Package2Product.objects.filter(product_id=product_id, package_id=package_id).delete()


def product2package_edit_update(product_list, package_id):
    """
    处理修改后套餐中商品是否处在Product2Package表中
    :param product_list: 用户选择商品id
    :param package_obj: 套餐id
    :return:
    """
    Product2Packaget_obj = models.Product2Package.objects.filter(package_id=package_id).values_list(
        'product_id').all()
    product2package_list = []
    for product2package in Product2Packaget_obj:
        product2package_list.append(str(product2package[0]))
    product2package_list_set = set(product2package_list)
    product_list_set = set(product_list)
    # 左交集
    left_intersection = product_list_set - product2package_list_set
    if left_intersection:
        for product_id in left_intersection:
            models.Product2Package.objects.create(product_id=product_id, package_id=package_id)
    # 有交集
    right_intersection = product2package_list_set - product_list_set
    if right_intersection:
        for product_id in right_intersection:
            models.Product2Package.objects.filter(product_id=product_id, package_id=package_id).delete()
