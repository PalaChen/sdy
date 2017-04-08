from . import models

def update_info(tb_name,nid):
    obj = tb_name.objects.filter(id=nid).first()
    return obj