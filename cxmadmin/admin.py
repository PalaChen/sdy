class BaseCxmAdmin(object):
    def __init__(self):
        self.actions.extend(self.default_actions)

    list_display = ()
    list_filter = []
    search_fields = []
    readonly_fields = []
    filter_horizontal = []
    list_per_page = 20
    default_actions = ['batch_deletion']
    actions = []
    actions_name = {'batch_deletion': '批量删除'}

    def batch_deletion(self, request, querysets):
        querysets.delete()
        return True


class AdminSite(object):
    def __init__(self):
        # 全局大字典
        # enabled_admins={'app名字':{'表名':'表对应的内存地址'}
        # enabled_admins={'app名字':{'Employee':'EmployeeAdmin'}
        # {'app名字':['表名','表名1]}
        self.enabled_admins = {}

    def register(self, model_class, admin_class=None):
        """注册admin表"""

        app_name = model_class._meta.app_label
        model_name = model_class._meta.model_name
        if not admin_class:  # 为了避免多个model共享同一个BaseCxmAdmin内存对象
            admin_class = BaseCxmAdmin()
        else:
            admin_class = admin_class()

        admin_class.model = model_class  # 把model_class赋值给了admin_class

        if app_name not in self.enabled_admins:
            self.enabled_admins[app_name] = {}

        self.enabled_admins[app_name][model_name] = admin_class


site = AdminSite()
