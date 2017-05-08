from . import models


def Add_info(tb_name, data):
    # try:
    res = tb_name.objects.filter(phone=data['phone']).first()
    if not res:
        print(data)
        res_obj = tb_name.objects.create(**data)
        return res_obj
    # except Exception as e:
    #     return e
