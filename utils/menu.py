from reposition import models

def get_cate_dic():
    """
    获取分类信息
    :param cate_list:
    :return:
    """
    cate_list = models.ProductCategory.objects.all()
    cate_dic = {}
    for row in cate_list:
        if row.cate_rootid == 0 and row.cate_parentid == 0:
            cate_dic.update({(row.id, row.cate_name): {}})
        elif row.cate_rootid != 0:
            for k in cate_dic.keys():
                if k[0] == row.cate_rootid:
                    # print(cate_tuple[k])
                    cate_dic[k].update({(row.id, row.cate_name): []})
        else:
            for k in cate_dic.keys():
                for k1 in cate_dic[k].keys():
                    if k1[0] == row.cate_parentid:
                        cate_dic[k][k1].append((row.id, row.cate_name))

    return cate_dic