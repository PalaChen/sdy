from . import models


def query_del(req, tb_name, nid):
    if req.method == 'GET':
        try:
            tb_name.objects.filter(id=nid).delete()
            return '成功'
        except Exception as e:
            print(e)
            return e
