from cxmadmin import admin
from reposition import models


class MyTaskAdmin(admin.BaseCxmAdmin):
    list_display = ['order', 'ctime']


class ClientInfoAdmin(admin.BaseCxmAdmin):
    list_display = ['name', 'mobile', 'source', 'group', 'employee', 'is_reg', 'user']
    list_filter = ['source', 'group', 'is_reg']
    search_fields = ['name', 'mobile']
    readonly_fields = ['status']


class UsersAdmin(admin.BaseCxmAdmin):
    list_display = ['name', 'email', 'phone', 'balance', 'voucher', 'qq', 'wechat', 'referrer', 'know',
                    'reg_time', 'remark', 'address']
    list_filter = ['know']
    search_fields = ['name', 'email', 'phone']
    readonly_fields = ['name', 'password', 'email', 'phone', 'balance', 'voucher', 'province', 'city', 'area',
                       'source', 'know', 'reg_employee', 'last_time']


class EmployeesAdmin(admin.BaseCxmAdmin):
    list_display = ['email', 'name', 'job_number', 'department', 'position', 'phone', 'qq', 'wechat', 'gender',
                    'birthday', 'entry_time', 'last_time']
    list_filter = ['gender', 'department', 'position', ]
    search_fields = ['name', 'department', 'position', 'phone']
    readonly_fields = ['last_time', 'reg_time', 'last_ip', 'role']


class ProductCategoryAdmin(admin.BaseCxmAdmin):
    list_display = ['name', 'count', 'employee', 'sort', 'date', ]
    list_filter = ['employee']
    search_fields = ['name']


class ProductsAdmin(admin.BaseCxmAdmin):
    list_display = ['p_name', 'p_price', 'p_market_price', 'p_putaway', 'p_ctime', 'p_top']
    list_filter = ['p_putaway', 'p_top']
    search_fields = ['p_name']


class OrderPaymentAdmin(admin.BaseCxmAdmin):
    list_display = ['order_code', 'user', 'status', 'total_price', 'coupon_price', 'pay_price', 'payment', 'ctime',
                    'ftime']
    list_filter = ['status', 'payment']
    search_fields = ['order_code', 'user']


class OrderSericeAdmin(admin.BaseCxmAdmin):
    list_display = ['order', 'status', 'allocation_status', 'ctime', 'start_time', 'end_time']
    list_filter = ['status', 'allocation_status']
    search_fields = ['order']


class IndexNavAdmin(admin.BaseCxmAdmin):
    list_display = ['id', 'name', 'url', 'status', 'weight', 'employee', 'ctime']
    list_filter = ['status', 'employee']
    search_fields = ['name', 'employee']


class ArticlesAdmin(admin.BaseCxmAdmin):
    list_display = ['id', 'title', 'author', 'category', 'comments', 'views', 'status', 'is_top', 'ctime']
    list_filter = ['status', 'is_top']
    search_fields = ['title', 'author', 'category']
    actions = []


class PositionAdmin(admin.BaseCxmAdmin):
    list_display = ['name', 'department', 'description']
    list_filter = ['department']
    search_fields = ['name']


class RegionalManagementAdmin(admin.BaseCxmAdmin):
    list_display = ['id', 'name']


admin.site.register(models.MyTask, MyTaskAdmin)
admin.site.register(models.ClientInfo, ClientInfoAdmin)
admin.site.register(models.Users, UsersAdmin)

admin.site.register(models.Employees, EmployeesAdmin)
admin.site.register(models.Role, EmployeesAdmin)
admin.site.register(models.Products, ProductsAdmin)
admin.site.register(models.ProductCategory, ProductCategoryAdmin)
admin.site.register(models.ProductService)
admin.site.register(models.ProductTImage)

admin.site.register(models.Articles, ArticlesAdmin)
# admin.site.register(models.ArticlesDetails)
admin.site.register(models.ArticlesCategory)
admin.site.register(models.ArticlesTag)
admin.site.register(models.Author)
admin.site.register(models.Menu)
admin.site.register(models.Bxslider)
admin.site.register(models.IndexNav)
admin.site.register(models.MessagesSend)
admin.site.register(models.MessagesVerifyCode)
admin.site.register(models.Orders)
admin.site.register(models.OrderSerice, OrderSericeAdmin)
admin.site.register(models.Process)
admin.site.register(models.ProcessName)
admin.site.register(models.ProcessStep)
admin.site.register(models.OrderPayment, OrderPaymentAdmin)
admin.site.register(models.PaymengAlipy, )
admin.site.register(models.IndexNav, IndexNavAdmin)
admin.site.register(models.Position, PositionAdmin)
admin.site.register(models.RegionalManagement, RegionalManagementAdmin)