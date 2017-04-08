from . import models


def query_del(tb_name, nid):
    try:
        tb_name.objects.filter(id=nid).delete()
        return True
    except Exception as e:
        return e
