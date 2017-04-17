from django.db import models


class Articles(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    summary = models.CharField(max_length=300, blank=True, null=True)
    ctime = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    author = models.ForeignKey('Author', models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey('ArticlesCategory', models.DO_NOTHING, blank=True, null=True)
    comments = models.IntegerField(blank=True, null=True, default=0)
    views = models.IntegerField(blank=True, null=True, default=0)
    status_choice = [(-1, '审核'), (0, '草稿'), (1, '公开')]
    status = models.IntegerField(blank=True, null=True, choices=status_choice)
    is_top = models.IntegerField(blank=True, null=True)
    p_url = models.CharField(max_length=100)

    class Meta:
        db_table = 'articles'


class ArticlesCategory(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    sort = models.IntegerField(blank=True, null=True)
    root_id = models.IntegerField(blank=True, null=True, default=0)
    parent_id = models.IntegerField(blank=True, null=True, default=0)
    ctime = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    author = models.ForeignKey('Author', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'articles_category'


class ArticlesComements(models.Model):
    content = models.TextField(blank=True, null=True)
    ctime = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    root_id = models.IntegerField(blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    article = models.ForeignKey(Articles, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'articles_comements'


class ArticlesDetails(models.Model):
    content = models.TextField(blank=True, null=True)
    article = models.OneToOneField(Articles, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'articles_details'


class ArticlesPraise(models.Model):
    praise = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    articles = models.ForeignKey(Articles, models.DO_NOTHING, blank=True, null=True)
    ctime = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        db_table = 'articles_praise'


class ArticlesTag(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    counts = models.IntegerField(blank=True, null=True, default=0)
    author = models.ForeignKey('Author', models.DO_NOTHING, blank=True, null=True)
    ctime = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        db_table = 'articles_tag'


class ArticlesToTag(models.Model):
    article = models.ForeignKey(Articles, models.DO_NOTHING, blank=True, null=True)
    tag = models.ForeignKey(ArticlesTag, models.DO_NOTHING, blank=True, null=True)
    ctime = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        db_table = 'articles_to_tag'


class Author(models.Model):
    counts = models.IntegerField(blank=True, null=True, default=0)
    views = models.IntegerField(blank=True, null=True, default=0)
    name = models.CharField(max_length=40, blank=True, null=True)
    ctime = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    employee = models.ForeignKey('Employees', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'authors'


class Bxslider(models.Model):
    status_choice = ((0, '下架'), (1, '上架'))
    status = models.IntegerField(blank=True, null=True, default=1, choices=status_choice)
    name = models.CharField(max_length=50, blank=True, null=True)
    img = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=100, )
    weight = models.IntegerField(blank=True, null=True, default=0)
    create_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    employee = models.ForeignKey('Employees', models.DO_NOTHING, blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'bxslider'


class Employees(models.Model):
    password = models.CharField(max_length=40, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    reg_time = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    last_time = models.DateTimeField(blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    qq = models.CharField(max_length=15, blank=True, null=True)
    wechat = models.CharField(max_length=30, blank=True, null=True)
    entry_time = models.DateTimeField(blank=True, null=True)
    birthday = models.IntegerField(blank=True, null=True)
    department = models.CharField(max_length=30, blank=True, null=True)
    position = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=4, blank=True, null=True)
    job_number = models.CharField(max_length=8, blank=True, null=True)
    last_ip = models.CharField(max_length=20, blank=True, null=True)
    role = models.ForeignKey('Role', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'employees'


class MessagesSend(models.Model):
    m_status = models.IntegerField(db_column='m_Status', blank=True, null=True)
    m_response_time = models.CharField(db_column='m_Response_Time', max_length=30, blank=True,
                                       null=True)
    m_messageid = models.CharField(db_column='m_MessageID', max_length=30, blank=True,
                                   null=True)
    m_order_id = models.CharField(db_column='m_Order_ID', max_length=15, blank=True,
                                  null=True)
    m_text = models.CharField(db_column='m_Text', max_length=2000, blank=True, null=True)
    m_phone = models.CharField(db_column='m_Phone', max_length=11, blank=True, null=True)
    m_employee_id = models.IntegerField(db_column='m_Employee_ID', blank=True, null=True)
    m_send_date = models.DateTimeField(db_column='m_Send_Date', blank=True, null=True,
                                       auto_now_add=True)

    class Meta:
        db_table = 'messages_send'


class MessagesVerifyCode(models.Model):
    m_status = models.IntegerField(db_column='m_Status', blank=True, null=True)
    m_response_time = models.CharField(db_column='m_Response_Time', max_length=30, blank=True, null=True)
    m_messageid = models.CharField(db_column='m_MessageID', max_length=30, blank=True, null=True)
    m_text = models.CharField(db_column='m_Text', max_length=300, blank=True, null=True)
    m_phone = models.CharField(max_length=11, db_column='m_Phone', blank=True, null=True)
    m_send_date = models.DateTimeField(db_column='m_Send_Date', blank=True, null=True, auto_now_add=True)
    m_verifycode = models.IntegerField(db_column='m_verifyCode', blank=True, null=True)
    m_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='m_User_id', blank=True, null=True)

    class Meta:
        db_table = 'messages_verify_code'


class OrderPayment(models.Model):
    order_code = models.CharField(max_length=18)
    status_choice = ((0, '待支付'), (1, '支付成功'), (2, '支付失败'))
    status = models.IntegerField(choices=status_choice, default=0)
    coupon = models.IntegerField()
    total_price = models.IntegerField()
    price = models.FloatField()
    payment_choice = ((0, '支付宝'), (1, '微信'), (2, '线下支付'), (3, '网银支付'))
    payment = models.CharField(max_length=20, null=True, choices=payment_choice)
    user = models.ForeignKey('Users', models.DO_NOTHING, )
    ctime = models.DateTimeField(null=True, auto_now_add=True)
    ftime = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'order_payment'


class Orders(models.Model):
    product_id = models.IntegerField(blank=True, null=True)
    product_name = models.CharField(max_length=100, blank=True, null=True)
    order_code = models.CharField(max_length=18, blank=True, null=True)
    ctime = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    cprice = models.FloatField(db_column='cPrice', blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    coupon = models.FloatField(blank=True, null=True, default=0)
    voucher = models.FloatField(blank=True, null=True, default=0)
    total_price = models.FloatField(blank=True, null=True)
    order_state_choice = ((0, '待付款'), (1, '待服务'), (2, '服务中'), (3, '服务完成'))
    order_state = models.CharField(max_length=24, choices=order_state_choice, default=0)

    pay_number = models.IntegerField(blank=True, null=True)
    pay_time = models.DateTimeField(blank=True, null=True)
    username = models.CharField(max_length=20, blank=True, null=True)
    user = models.ForeignKey('Users')
    name = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    order_process = models.CharField(max_length=20, blank=True, null=True)
    remark = models.CharField(max_length=600, blank=True, null=True)
    category = models.CharField(max_length=30, blank=True, null=True)
    province = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    area = models.CharField(max_length=20, blank=True, null=True)
    employee = models.ForeignKey(Employees, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'orders'


class Process(models.Model):
    order_id = models.IntegerField(blank=True, null=True)
    process_name = models.CharField(max_length=30, blank=True, null=True)
    step_name = models.CharField(max_length=30, blank=True, null=True)
    employee_name = models.CharField(max_length=30, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    re_mark = models.CharField(max_length=500, blank=True, null=True)
    employee = models.ForeignKey(Employees, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'process'


class ProcessName(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    employee_name = models.CharField(max_length=30, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    modify_time = models.DateTimeField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True, default=1)
    employee = models.ForeignKey(Employees, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'process_name'


class ProcessStep(models.Model):
    process_name = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    employee_name = models.CharField(max_length=30, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    modify_time = models.DateTimeField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True, default=1)
    p_name = models.ForeignKey(ProcessName, models.DO_NOTHING, blank=True, null=True)
    employee = models.ForeignKey(Employees, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'process_step'


class ProductCImage(models.Model):
    ul_name = models.CharField(db_column='ul_Name', max_length=100, blank=True, null=True)
    ul_sourcename = models.CharField(db_column='ul_SourceName', max_length=30, blank=True,
                                     null=True)
    ul_type = models.CharField(db_column='ul_Type', max_length=10, blank=True, null=True)
    ul_size = models.IntegerField(db_column='ul_Size', blank=True, null=True)
    ul_posttime = models.DateTimeField(db_column='ul_PostTime', blank=True, null=True,
                                       auto_now_add=True)
    ul_employee = models.ForeignKey(Employees, models.DO_NOTHING, db_column='ul_Employee_id', blank=True,
                                    null=True)
    ul_product = models.ForeignKey('Products', models.DO_NOTHING, blank=True, null=True)
    ul_url = models.CharField(db_column='ul_Url', max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'product_c_image'


class ProductCategory(models.Model):
    cate_name = models.CharField(db_column='cate_Name', max_length=10, blank=True,
                                 null=True)
    cate_count = models.IntegerField(db_column='cate_Count', blank=True, null=True, default=0)
    cate_date = models.DateTimeField(db_column='cate_Date', blank=True, null=True,
                                     auto_now_add=True)
    cate_employee = models.ForeignKey(Employees, models.DO_NOTHING, db_column='cate_Employee_id', blank=True,
                                      null=True)
    cate_rootid = models.IntegerField(db_column='cate_RootID', blank=True, null=True, default=0)
    cate_parentid = models.IntegerField(db_column='cate_ParentID', blank=True, null=True, default=0)
    cate_sort = models.IntegerField(db_column='cate_Sort', blank=True, null=True)

    class Meta:
        db_table = 'product_category'


class ProductService(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    reminder_choices = ((0, '不提醒'), (1, '提醒'))
    renewal_reminder = models.IntegerField(choices=reminder_choices, blank=True, null=True)
    ctime = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    employee = models.ForeignKey(Employees, models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey(ProductCategory, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'product_service'


class ProductTImage(models.Model):
    ul_name = models.CharField(db_column='ul_Name', max_length=50, blank=True, null=True)
    ul_sourcename = models.CharField(db_column='ul_SourceName', max_length=30, blank=True, null=True)
    ul_type = models.CharField(db_column='ul_Type', max_length=10, blank=True, null=True)
    ul_size = models.IntegerField(db_column='ul_Size', blank=True, null=True)
    ul_posttime = models.DateTimeField(db_column='ul_PostTime', blank=True, null=True, auto_now_add=True)
    ul_employee = models.ForeignKey(Employees, models.DO_NOTHING, db_column='ul_Employee_id', blank=True, null=True)
    ul_product = models.ForeignKey('Products', models.DO_NOTHING, db_column='ul_Product_id', related_name='pro_image',
                                   blank=True, null=True)
    ul_url = models.CharField(db_column='ul_Url', max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'product_t_image'


class Products(models.Model):
    p_name = models.CharField(db_column='p_Name', max_length=50, blank=True, null=True)
    p_price = models.FloatField(db_column='p_Price', blank=True, null=True)
    p_market_price = models.FloatField(db_column='p_Market_Price', blank=True, null=True)
    p_details = models.TextField(db_column='p_Details', blank=True, null=True)
    putaway_name = ((0, '下线'), (1, '上线'))
    p_putaway = models.IntegerField(db_column='p_Putaway', choices=putaway_name, blank=True, null=True, default=1)
    p_seo_title = models.CharField(db_column='p_Seo_Title', max_length=80, blank=True,
                                   null=True)
    p_seo_keyword = models.CharField(db_column='p_Seo_Keyword', max_length=100, blank=True,
                                     null=True)
    p_seo_description = models.CharField(db_column='p_Seo_Description', max_length=200, blank=True,
                                         null=True)
    p_ctime = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    p_category = models.ForeignKey(ProductCategory, models.DO_NOTHING, db_column='p_Category_id', blank=True, null=True)
    p_top = models.IntegerField(db_column='p_Top', blank=True, null=True, default=0)
    p_employee = models.ForeignKey(Employees, models.DO_NOTHING, db_column='p_Employee_id', blank=True, null=True)
    p_service = models.OneToOneField('ProductService', models.DO_NOTHING, blank=True, null=True)
    p_business = models.ForeignKey('ProcessName', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'products'


class Users(models.Model):
    username = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=40, )
    email = models.CharField(max_length=100, )
    phone = models.CharField(max_length=11, )
    name = models.CharField(max_length=30, )
    qq = models.CharField(max_length=15, null=True)
    wechat = models.CharField(max_length=30, blank=True, null=True)
    group = models.CharField(max_length=30, blank=True, null=True)
    reg_time = models.DateTimeField(blank=True, auto_now_add=True)
    last_time = models.DateTimeField(blank=True, null=True)
    remark = models.CharField(max_length=300, blank=True, null=True)
    referrer = models.CharField(max_length=30, blank=True, null=True)
    balance = models.FloatField(blank=True, null=True)
    voucher = models.FloatField(blank=True, null=True)
    province = models.IntegerField(blank=True, null=True, default=0)
    city = models.IntegerField(blank=True, null=True, default=0)
    area = models.IntegerField(blank=True, null=True, default=0)
    address = models.CharField(blank=True, null=True, max_length=100)
    source = models.CharField(blank=True, null=True, max_length=30)
    know = models.IntegerField(blank=True, null=True, default=0)
    reg_employee = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'users'


class IndexNav(models.Model):
    name = models.CharField(max_length=100)
    weight = models.IntegerField()
    url = models.CharField(max_length=100)
    status_choice = ((0, '下线'), (1, '上线'))
    status = models.BooleanField(default=1, choices=status_choice)
    employee = models.ForeignKey('Employees')
    ctime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'indexnavs'


class Role(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'roles'


class Employee2Role(models.Model):
    employee = models.ForeignKey('Employees')
    role = models.ForeignKey('Role')

    class Meta:
        db_table = 'employee2role'

    def __str__(self):
        return "%s-%s" % (self.employee.employee, self.role.caption,)


# 操作表
class Action(models.Model):
    # get  获取用户信息1
    # post  创建用户2
    # delete 删除用户3
    # put  修改用户4
    caption = models.CharField(max_length=32)
    code = models.CharField(max_length=32)

    class Meta:
        db_table = 'action'

    def __str__(self):
        return self.caption


# 菜单表
class Menu(models.Model):
    caption = models.CharField(max_length=32)
    parent = models.ForeignKey('self', related_name='menu_p', null=True, blank=True)
    weight = models.IntegerField(default=0)

    class Meta:
        db_table = 'menu'

    def __str__(self):
        return "%s" % (self.caption,)


# 权限表
class Permission(models.Model):
    caption = models.CharField(max_length=32)
    url = models.CharField(max_length=32)
    menu = models.ForeignKey(Menu, null=True, blank=True)
    weight = models.IntegerField(default=0)

    class Meta:
        db_table = 'permission'

    def __str__(self):
        return "%s-%s" % (self.caption, self.url,)


# 权限表——实际操作
class Permission2Action(models.Model):
    permission = models.ForeignKey(Permission)
    action = models.ForeignKey(Action)

    class Meta:
        db_table = 'permission2action'

    def __str__(self):
        return "%s-%s:-%s?t=%s" % (self.permission.caption, self.action.caption, self.permission.url, self.action.code,)


# 角色分配权限
class Permission2Action2Role(models.Model):
    p2a = models.ForeignKey(Permission2Action)
    role = models.ForeignKey(Role)

    class Meta:
        db_table = 'permission2action2role'

    def __str__(self):
        return "%s==>%s" % (self.role.caption, self.p2a,)


class Provinces(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        db_table = 'china_provinces'


class Citys(models.Model):
    name = models.CharField(max_length=12)
    p = models.ForeignKey(Provinces)
    zipcode = models.IntegerField()

    class Meta:
        db_table = 'china_city'


class Districts(models.Model):
    name = models.CharField(max_length=12)
    c = models.ForeignKey(Citys)

    class Meta:
        db_table = 'china_districts'
