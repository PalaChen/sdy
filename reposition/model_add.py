from . import models


def Add_info(tb_name, data):
    try:
        password = data['password']
        phone = data['phone']
        res =tb_name.objects.filter(phone=phone).first()
        if not res:
            tb_name.objects.create(phone=phone, password=password)
            return True
        return '该手机号码已存在'
    except Exception as e:
        return e

