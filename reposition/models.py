from django.db import models


class Articles(models.Model):
    """
    文章表
    """
    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=300)
    ctime = models.DateTimeField(null=True, auto_now_add=True)
    author = models.ForeignKey('Author')
    category = models.ForeignKey('ArticlesCategory')
    comments = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    status_choice = ((-1, '审核'), (0, '草稿'), (1, '公开'))
    status = models.SmallIntegerField(null=True, choices=status_choice)
    is_top_choice = ((0, '置顶'), (1, '不置顶'))
    is_top = models.BooleanField(default=0, choices=is_top_choice)
    p_url = models.CharField(max_length=100)
    cover_image = models.ForeignKey('ArticlesCoverImage', null=True)

    class Meta:
        db_table = 'articles'
        verbose_name = '文章表'
        verbose_name_plural = '文章表'


class ArticlesCoverImage(models.Model):
    """
    文章封面图
    """
    ul_name = models.CharField(max_length=255, null=True)
    ul_sourcename = models.CharField(max_length=255, null=True)
    ul_type = models.CharField(max_length=10, null=True)
    ul_size = models.IntegerField(null=True)
    ul_posttime = models.DateTimeField(auto_now_add=True)
    ul_employee = models.ForeignKey('Employees')
    ul_url = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'articles_cover_image'
        verbose_name = "文章封面图"
        verbose_name_plural = "文章封面图"


class ArticlesCategory(models.Model):
    """
    文章分类
    """
    name = models.CharField(max_length=50)
    sort = models.IntegerField(null=True)
    root_id = models.IntegerField(default=0)
    parent_id = models.IntegerField(default=0)
    ctime = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('Author')

    class Meta:
        db_table = 'articles_category'
        verbose_name = '文章分类表'
        verbose_name_plural = '文章分类表'

    def __str__(self):
        return self.name


class ArticlesComements(models.Model):
    """
    文章评论
    """
    content = models.TextField()
    ctime = models.DateTimeField(auto_now_add=True)
    root_id = models.IntegerField(null=True)
    parent_id = models.IntegerField(null=True)
    article = models.ForeignKey(Articles)
    user = models.ForeignKey('Users')

    class Meta:
        db_table = 'articles_comements'
        verbose_name = '文章评论表'
        verbose_name_plural = '文章评论表'


class ArticlesDetails(models.Model):
    """
    文章内容
    """
    content = models.TextField()
    article = models.OneToOneField(Articles)

    class Meta:
        db_table = 'articles_details'
        verbose_name = '文章内容表'
        verbose_name_plural = '文章内容表'


class ArticlesPraise(models.Model):
    """
    文章点赞
    """
    praise = models.SmallIntegerField(null=True)
    user = models.ForeignKey('Users')
    articles = models.ForeignKey(Articles)
    ctime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'articles_praise'
        verbose_name = '文章点赞表'
        verbose_name_plural = '文章点赞表'


class ArticlesTag(models.Model):
    """
    文章标签
    """
    name = models.CharField(max_length=50, )
    counts = models.IntegerField(default=0)
    author = models.ForeignKey('Author')
    ctime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'articles_tag'
        verbose_name = '文章标签表'
        verbose_name_plural = '文章标签表'


class ArticlesToTag(models.Model):
    """
    文章对应的标签
    """
    article = models.ForeignKey(Articles, models.DO_NOTHING)
    tag = models.ForeignKey(ArticlesTag, models.DO_NOTHING)
    ctime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'articles_to_tag'
        verbose_name = "文章对应的标签表"
        verbose_name_plural = "文章对应的标签表"


class Author(models.Model):
    """
    作者表
    """
    counts = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    name = models.CharField(max_length=40, )
    ctime = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey('Employees')

    class Meta:
        db_table = 'authors'
        verbose_name = "作者表"
        verbose_name_plural = "作者表"

    def __str__(self):
        return self.name


class Bxslider(models.Model):
    """
    首页轮播图
    """
    status_choice = ((0, '下架'), (1, '上架'))
    status = models.BooleanField(default=1, choices=status_choice)
    name = models.CharField(max_length=50)
    img = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    weight = models.IntegerField(default=0)
    create_date = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey('Employees')
    size = models.IntegerField(null=True)

    class Meta:
        db_table = 'bxslider'
        verbose_name = "首页轮播图表"
        verbose_name_plural = "首页轮播图表"


class Employees(models.Model):
    """
    员工表
    """
    email = models.CharField(max_length=100, verbose_name='邮箱')
    name = models.CharField(max_length=30, verbose_name='姓名')
    password = models.CharField(max_length=40, )
    phone = models.CharField(max_length=11, verbose_name='手机')
    qq = models.CharField(max_length=15, null=True, blank=True, verbose_name='QQ')
    wechat = models.CharField(max_length=30, null=True, blank=True, verbose_name='微信')
    entry_time = models.DateField(null=True, blank=True, verbose_name='入职时间')
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    department = models.ForeignKey('Department', null=True, verbose_name='部门')
    position = models.ForeignKey('Position', null=True, verbose_name='职位')
    gender_choice = ((0, '男'), (1, '女'))
    gender = models.SmallIntegerField(choices=gender_choice, null=True, verbose_name='性别')
    job_number = models.CharField(max_length=8, null=True, verbose_name='工号', unique=True)
    role = models.ForeignKey('Role', null=True, blank=True, verbose_name='权限角色')
    reg_time = models.DateField(auto_now_add=True, verbose_name='注册时间')
    last_ip = models.CharField(max_length=20, null=True, blank=True)
    last_time = models.DateTimeField(null=True, blank=True, verbose_name='上一次登陆')
    status_choices = ((0, '真实'), (1, '虚假'))
    status = models.SmallIntegerField(default=0, blank=True, choices=status_choices)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'employees'
        verbose_name = "员工表"
        verbose_name_plural = "员工表"


class MessagesSend(models.Model):
    """
    短信发送
    """
    status = models.SmallIntegerField()
    response_time = models.CharField(max_length=30)
    message_id = models.CharField(max_length=30)
    content = models.CharField(max_length=1000)
    phone = models.CharField(max_length=11)
    order = models.ForeignKey('Orders')
    employee = models.ForeignKey('Employees')
    ctime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages_send'
        verbose_name = "短信发送表"
        verbose_name_plural = "短信发送表"


class MessagesVerifyCode(models.Model):
    """
    验证码短信
    """
    m_status = models.IntegerField(db_column='m_Status')
    m_response_time = models.CharField(db_column='m_Response_Time', max_length=30)
    m_messageid = models.CharField(db_column='m_MessageID', max_length=30)
    m_text = models.CharField(db_column='m_Text', max_length=300, )
    m_phone = models.CharField(max_length=11, db_column='m_Phone')
    m_send_date = models.DateTimeField(db_column='m_Send_Date', auto_now_add=True)
    m_verifycode = models.IntegerField(db_column='m_verifyCode', )
    m_user = models.ForeignKey('Users', db_column='m_User_id', null=True)

    class Meta:
        db_table = 'messages_verify_code'
        verbose_name = "验证码短信表"
        verbose_name_plural = "验证码短信表"


class Orders(models.Model):
    """
    订单表
    """
    product_id = models.IntegerField(blank=True)
    product_name = models.CharField(max_length=100, blank=True)
    order_code = models.CharField(max_length=18, )
    ctime = models.DateTimeField(auto_now_add=True)
    cprice = models.FloatField(db_column='cPrice')
    number = models.IntegerField(default=1)
    coupon = models.FloatField(default=0)
    voucher = models.FloatField(default=0)
    total_price = models.FloatField()
    order_state_choice = ((0, '待付款'), (1, '待服务'), (2, '服务中'),
                          (3, '交易关闭'), (4, '服务完成'), (5, '退款中'),
                          (6, '退款完成'),)
    order_state = models.SmallIntegerField(choices=order_state_choice, default=0)
    type_choice = ((0, '真实'), (1, '虚假'))
    type = models.SmallIntegerField(choices=order_state_choice, default=0)
    username = models.CharField(max_length=20, null=True)
    user = models.ForeignKey('Users')
    name = models.CharField(max_length=30, )
    phone = models.CharField(max_length=11, )
    order_process = models.CharField(max_length=20, null=True)
    remark = models.CharField(max_length=600, null=True)
    # 服务分类
    category = models.CharField(max_length=30, null=True)
    # 业务ID
    p_business = models.ForeignKey('ProcessStep')
    province = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=64, null=True)
    area = models.CharField(max_length=64, null=True)
    employee = models.ForeignKey(Employees, models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'orders'
        verbose_name = "订单表"
        verbose_name_plural = "订单表"

    def __str__(self):
        return self.order_code


class OrderPayment(models.Model):
    """
    支付信息
    """
    order_code = models.CharField(max_length=18, verbose_name='订单号', unique=True)
    user = models.ForeignKey('Users', verbose_name='支付用户')
    status_choice = ((0, '待支付'), (1, '支付成功'), (2, '支付失败'), (3, '交易关闭'))
    status = models.SmallIntegerField(choices=status_choice, default=0, verbose_name='支付状态')
    total_price = models.FloatField(verbose_name='总价格')
    coupon_price = models.IntegerField(default=0, verbose_name='优惠价格')
    pay_price = models.FloatField(default=0, verbose_name='支付价格')
    payment_choice = ((0, '支付宝'), (1, '微信'), (2, '线下支付'), (3, '网银支付'))
    payment = models.SmallIntegerField(choices=payment_choice, null=True, verbose_name='支付方式')
    ctime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    ftime = models.DateTimeField(null=True, verbose_name='支付时间')

    class Meta:
        db_table = 'orders_payment'
        verbose_name = "支付记录表"
        verbose_name_plural = "支付记录表"


class PaymengAlipy(models.Model):
    """
    阿里支付
    """
    pay = models.ForeignKey('OrderPayment')
    out_trade_no = models.CharField(max_length=20, verbose_name='订单号')
    trade_no = models.CharField(max_length=30, verbose_name='支付宝单号')
    trade_status = models.CharField(max_length=18, verbose_name='交易状态')
    payment_type = models.SmallIntegerField(verbose_name='交易方式')
    notify_time = models.CharField(max_length=25, verbose_name='交易时间')
    is_success = models.CharField(max_length=5, verbose_name='成功状态')
    notify_type = models.CharField(max_length=20, verbose_name='通知类型')
    buyer_id = models.CharField(max_length=16, verbose_name='用户标识')
    buyer_email = models.CharField(max_length=64, verbose_name='买家邮箱')
    total_fee = models.FloatField(verbose_name='交易金额')

    class Meta:
        db_table = 'orders_payment_alipy'
        verbose_name = "支付宝支付信息表"
        verbose_name_plural = "支付宝支付信息表"


class OrderSerice(models.Model):
    order = models.OneToOneField('Orders', verbose_name='订单号')
    status_choice = ((0, '未开始'), (1, '开始服务'), (2, '服务中'), (3, '暂定服务'), (4, '服务结束'))
    # 订单状态
    status = models.SmallIntegerField(choices=status_choice, default=0, verbose_name='服务状态')
    # 分配状态
    allocation_status_choices = ((0, '未分配'), (1, '已分配'))
    allocation_status = models.SmallIntegerField(default=False, choices=allocation_status_choices, verbose_name='分配状态')
    ctime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    start_time = models.DateTimeField(null=True, verbose_name='分配时间')
    end_time = models.DateTimeField(null=True, verbose_name='完成时间')
    city = models.CharField(max_length=64, verbose_name='城市')
    area = models.CharField(max_length=64, verbose_name='地区')

    class Meta:
        db_table = 'order_serice'
        verbose_name = "订单服务分配表"
        verbose_name_plural = "订单服务分配表"


class Process(models.Model):
    """
    订单具体进展
    """
    order = models.ForeignKey('Orders')
    process_name = models.CharField(max_length=30, )
    step_name = models.CharField(max_length=30, )
    date = models.DateTimeField(auto_now_add=True)
    re_mark = models.TextField(null=True)
    employee_name = models.CharField(max_length=30)
    employee = models.ForeignKey(Employees, models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'process'
        verbose_name = "订单进展表"
        verbose_name_plural = "订单进展表"


class ProcessName(models.Model):
    """
    业务名
    """
    name = models.CharField(max_length=30, )
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(null=True)
    state = models.IntegerField(default=1)
    employee = models.ForeignKey(Employees, models.DO_NOTHING)

    class Meta:
        db_table = 'process_name'
        verbose_name = "订单进展名字表"
        verbose_name_plural = "订单进展名字表"


class ProcessStep(models.Model):
    """
    业务具体步骤
    """
    process_name = models.CharField(max_length=30, )
    name = models.CharField(max_length=30, )
    number = models.IntegerField()
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(null=True)
    state = models.IntegerField(default=1)
    p_name = models.ForeignKey(ProcessName, )
    employee = models.ForeignKey(Employees, )

    class Meta:
        db_table = 'process_step'
        verbose_name = "业务具体步骤表"
        verbose_name_plural = "业务具体步骤表"


class ProductCImage(models.Model):
    """
    产品内容图片
    """
    ul_name = models.CharField(db_column='ul_Name', max_length=100, null=True)
    ul_sourcename = models.CharField(db_column='ul_SourceName', max_length=30,
                                     null=True)
    ul_type = models.CharField(db_column='ul_Type', max_length=10, null=True)
    ul_size = models.IntegerField(db_column='ul_Size', null=True)
    ul_posttime = models.DateTimeField(db_column='ul_PostTime', null=True,
                                       auto_now_add=True)
    ul_employee = models.ForeignKey(Employees, db_column='ul_Employee_id', null=True)
    ul_product = models.ForeignKey('Products', null=True)
    ul_url = models.CharField(db_column='ul_Url', max_length=100, null=True)

    class Meta:
        db_table = 'product_c_image'
        verbose_name = "产品内容图片表"
        verbose_name_plural = "产品内容图片表"


class ProductCategory(models.Model):
    """
    产品分类
    """
    name = models.CharField(max_length=20, verbose_name='分类名字')
    count = models.IntegerField(db_column='cate_Count', default=0, verbose_name='文章数量')
    employee = models.ForeignKey(Employees, db_column='cate_Employee_id', verbose_name='创建员工')
    root_id = models.SmallIntegerField(db_column='cate_RootID', default=0, )
    parent_id = models.SmallIntegerField(db_column='cate_ParentID', default=0)
    sort = models.IntegerField(db_column='cate_Sort', default=0, verbose_name='权重')
    date = models.DateTimeField(db_column='cate_Date', auto_now_add=True, verbose_name='创建日期')

    class Meta:
        db_table = 'product_category'
        verbose_name = "产品分类表"
        verbose_name_plural = "产品分类表"


class ProductService(models.Model):
    """
    产品服务
    """
    name = models.CharField(max_length=20, )
    number = models.IntegerField(null=True)
    reminder_choices = ((0, '不提醒'), (1, '提醒'))
    renewal_reminder = models.SmallIntegerField(choices=reminder_choices, default=0)
    ctime = models.DateTimeField(auto_now_add=True)
    root = models.ForeignKey('self', null=True)
    employee = models.ForeignKey(Employees, models.DO_NOTHING, )
    category = models.ForeignKey(ProductCategory, null=True)

    class Meta:
        db_table = 'product_service'
        verbose_name = "产品服务表"
        verbose_name_plural = "产品服务表"


class ProductTImage(models.Model):
    """
    产品首图片
    """
    ul_name = models.CharField(db_column='ul_Name', max_length=255, null=True)
    ul_sourcename = models.CharField(db_column='ul_SourceName', max_length=255, null=True)
    ul_type = models.CharField(db_column='ul_Type', max_length=10, null=True)
    ul_size = models.IntegerField(db_column='ul_Size', null=True)
    ul_posttime = models.DateTimeField(db_column='ul_PostTime', auto_now_add=True)
    ul_employee = models.ForeignKey(Employees, db_column='ul_Employee_id', )
    ul_product = models.ForeignKey('Products', db_column='ul_Product_id', related_name='pro_image', null=True)
    ul_url = models.CharField(db_column='ul_Url', max_length=100, null=True)

    class Meta:
        db_table = 'product_t_image'
        verbose_name = "产品首图片表"
        verbose_name_plural = "产品首图片表"


class Products(models.Model):
    """
    产品表
    """
    p_name = models.CharField(db_column='p_Name', max_length=64, )
    p_price = models.FloatField(db_column='p_Price', )
    p_market_price = models.FloatField(db_column='p_Market_Price', null=True)
    p_details = models.TextField(db_column='p_Details', verbose_name='产品内容')
    p_putaway_choices = ((0, '下架'), (1, '上架'))
    p_putaway = models.SmallIntegerField(db_column='p_Putaway', choices=p_putaway_choices, default=1)
    p_top_choices = (0, '不推荐'), (1, '推荐')
    p_top = models.SmallIntegerField(db_column='p_Top', choices=p_top_choices, default=0)
    p_seo_keyword = models.CharField(db_column='p_Seo_Keyword', max_length=100, null=True)
    p_seo_description = models.CharField(db_column='p_Seo_Description', max_length=200, null=True)
    p_ctime = models.DateTimeField(null=True, auto_now_add=True)
    p_category = models.ForeignKey(ProductCategory, models.DO_NOTHING, db_column='p_Category_id', )
    p_employee = models.ForeignKey(Employees, models.DO_NOTHING, db_column='p_Employee_id', )
    p_service = models.ForeignKey('ProductService', null=True)
    p_business = models.ForeignKey('ProcessName', )
    city = models.ForeignKey('RegionalManagement', related_name='regional_city')
    area = models.ForeignKey('RegionalManagement', )

    class Meta:
        db_table = 'products'
        verbose_name = "产品表"
        verbose_name_plural = "产品表"


class Users(models.Model):
    """
    用户表
    """
    # username = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=11, unique=True, verbose_name='手机号码')
    email = models.CharField(max_length=100, blank=True, verbose_name='邮箱')
    name = models.CharField(max_length=30, verbose_name='称呼')
    password = models.CharField(max_length=40, verbose_name='密码')
    qq = models.CharField(max_length=15, null=True, blank=True, verbose_name='QQ')
    wechat = models.CharField(max_length=30, null=True, blank=True, verbose_name='微信')
    group = models.CharField(max_length=30, null=True, blank=True, verbose_name='分组')
    remark = models.CharField(max_length=300, null=True, blank=True, verbose_name='备注')
    referrer = models.CharField(max_length=30, null=True, blank=True, verbose_name='推荐')
    balance = models.FloatField(null=True, blank=True, verbose_name='余额')
    voucher = models.FloatField(null=True, blank=True, verbose_name='优惠卷')
    province = models.SmallIntegerField(null=True, blank=True, verbose_name='省')
    city = models.SmallIntegerField(null=True, blank=True, verbose_name='市')
    area = models.SmallIntegerField(null=True, blank=True, verbose_name='区')
    address = models.CharField(null=True, max_length=100, blank=True, verbose_name='地址')
    source = models.CharField(null=True, max_length=30, blank=True, verbose_name='来源')
    know_choice = ((1, '搜索引擎'), (2, '线下活动'), (3, '微信微博'), (4, '朋友土建'), (5, '名片传单'), (6, '其他'))
    know = models.SmallIntegerField(null=True, choices=know_choice, verbose_name='了解')
    reg_employee = models.IntegerField(null=True, blank=True, verbose_name='注册员工')
    reg_time = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='注册时间')
    last_time = models.DateTimeField(null=True, blank=True, verbose_name='最近登录')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'users'
        verbose_name = "用户表"
        verbose_name_plural = "用户表"


class UsersKeyword(models.Model):
    name = models.CharField(max_length=30, verbose_name='名字')

    class Meta:
        db_table = 'user_keyword'
        verbose_name = "用户关键词"
        verbose_name_plural = "用户关键词"


class MyTask(models.Model):
    order = models.ForeignKey('Orders', verbose_name='订单号')
    employee = models.ForeignKey('Employees', verbose_name='员工姓名')
    order_serice = models.ForeignKey('OrderSerice', verbose_name='服务订单')
    status_choices = ((0, '未完成'), (1, '已完成'))
    status = models.SmallIntegerField(default=0, blank=True, choices=status_choices)
    ctime = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='分配时间')

    class Meta:
        db_table = 'my_task'
        verbose_name = "我的任务"
        verbose_name_plural = "我的任务"


class IndexNav(models.Model):
    """
    首页导航
    """
    name = models.CharField(max_length=100, verbose_name='名称')
    weight = models.IntegerField(default=0, verbose_name='权重')
    url = models.CharField(max_length=100, verbose_name='网址')
    nav_status_choice = ((0, '下架'), (1, '上线'))
    status = models.SmallIntegerField(default=1, choices=nav_status_choice, verbose_name='状态')
    ishot_choice = ((0, '不热门'), (1, '热门'))
    ishot = models.SmallIntegerField(choices=ishot_choice, verbose_name='热门')
    employee = models.ForeignKey('Employees', verbose_name='创建人')
    ctime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'indexnavs'
        verbose_name = "导航表"
        verbose_name_plural = "导航表"


class Role(models.Model):
    """
    权限角色表
    """
    name = models.CharField(max_length=30, unique=True, verbose_name='名字')

    class Meta:
        db_table = 'roles'
        verbose_name = "权限角色表"
        verbose_name_plural = "权限角色表"

    def __str__(self):
        return self.name


class Employee2Role(models.Model):
    """
    员工和角色关系
    """
    employee = models.ForeignKey('Employees')
    role = models.ForeignKey('Role')

    class Meta:
        db_table = 'employee2role'

    def __str__(self):
        return "%s-%s" % (self.employee, self.role,)


# 操作表
class Action(models.Model):
    """
    操作表
    """
    # get  获取用户信息1
    # post  创建用户2
    # delete 删除用户3
    # put  修改用户4
    caption = models.CharField(max_length=64)
    code = models.CharField(max_length=64)

    class Meta:
        db_table = 'action'

    def __str__(self):
        return self.caption


# 菜单表
class Menu(models.Model):
    """
    后台菜单表
    """
    caption = models.CharField(max_length=32, unique=True)
    parent = models.ForeignKey('self', related_name='menu_p', null=True, blank=True)
    weight = models.IntegerField(default=0)

    class Meta:
        db_table = 'menu'
        verbose_name = "后台菜单表"
        verbose_name_plural = "后台菜单表"

    def __str__(self):
        return "%s" % (self.caption,)


# 权限表
class Permission(models.Model):
    """
    权限表
    """
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
    """
    权限表——实际操作
    """
    permission = models.ForeignKey(Permission)
    action = models.ForeignKey(Action)

    class Meta:
        db_table = 'permission2action'

    def __str__(self):
        return "%s-%s:-%s?t=%s" % (self.permission.caption, self.action.caption, self.permission.url, self.action.code,)


# 角色分配权限
class Permission2Action2Role(models.Model):
    """
    角色分配权限
    """
    p2a = models.ForeignKey(Permission2Action)
    role = models.ForeignKey(Role)

    class Meta:
        db_table = 'permission2action2role'

    def __str__(self):
        return "%s==>%s" % (self.role.caption, self.p2a,)


class ClientInfo(models.Model):
    name = models.CharField(max_length=30, verbose_name='客户姓名')
    mobile = models.CharField(max_length=11, verbose_name='客户手机')
    source_choices = ((0, 'web端'), (1, 'pc端'), (2, '微信'), (3, '推荐'))
    source = models.SmallIntegerField(choices=source_choices, verbose_name='客户来源')
    group_choices = ((0, '潜在客户'), (1, '意向客户'), (2, '无效用户'))
    group = models.SmallIntegerField(choices=group_choices, verbose_name='所属分组')
    employee = models.ForeignKey('Employees', verbose_name='归属人')
    is_reg_choices = ((0, '未注册'), (1, '已注册'))
    is_reg = models.SmallIntegerField(choices=is_reg_choices, verbose_name='是否注册')
    user = models.IntegerField(null=True, blank=True, verbose_name='客户账户')

    class Meta:
        db_table = 'client_info'
        verbose_name = '客户表'
        verbose_name_plural = '客户表'

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=30, verbose_name='部门')

    class Meta:
        db_table = 'department'
        verbose_name = '部门表'
        verbose_name_plural = '部门表'

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=20, verbose_name='职位')
    department = models.ForeignKey('Department', verbose_name='部门')
    # counts = models.SmallIntegerField(default=0, blank=True, verbose_name='人员数量')
    description = models.TextField(null=True, blank=True, verbose_name='岗位工作描述')

    class Meta:
        db_table = 'position'
        verbose_name = '职位表'
        verbose_name_plural = '职位表'

    def __str__(self):
        return self.name


class China(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'china'


class RegionalManagement(models.Model):
    city = models.ForeignKey('China')
    code = models.IntegerField()
    name = models.CharField(max_length=30)
    r_code = models.IntegerField(null=True)
    p_code = models.IntegerField(null=True)

    class Meta:
        db_table = 'regional_management'
        verbose_name = '区域管理'
        verbose_name_plural = '区域管理'

    def __str__(self):
        return self.name


class Product2area(models.Model):
    product = models.ForeignKey('Products')
    area = models.ForeignKey('RegionalManagement')
    p_price = models.FloatField(db_column='p_Price', )
    p_market_price = models.FloatField(db_column='p_Market_Price', null=True)

    class Meta:
        db_table = 'product_to_area'


class ProductRecommend(models.Model):
    product = models.ForeignKey('Products')
    name = models.CharField(max_length=64, verbose_name='产品名字')
    price = models.FloatField(verbose_name='价格')
    description = models.CharField(max_length=100, verbose_name='描述')
    status_choices = ((0, '推荐'), (1, '下线'))
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name='状态')

    class Meta:
        db_table = 'product_recommend'


# 产品套餐
class Package(models.Model):
    name = models.CharField(max_length=64, verbose_name='套餐名')
    status_choices = ((0, '下线'), (1, '上线'))
    status = models.SmallIntegerField(choices=status_choices, default=1, verbose_name='状态')
    weight = models.SmallIntegerField(default=0, verbose_name='权重')
    dscription = models.TextField(verbose_name='描述')
    cprice = models.FloatField(verbose_name='价格')
    original_price = models.FloatField(verbose_name='原价')
    employee = models.ForeignKey('Employees', verbose_name='创建人')
    area = models.ForeignKey('RegionalManagement', verbose_name='地区')
    cover_image = models.ForeignKey('ProductTImage', verbose_name='封面图', null=True, blank=True)

    class Meta:
        db_table = 'packages'


# 产品对应的套餐
class Product2Package(models.Model):
    product = models.ForeignKey('Products', null=True)
    package = models.ForeignKey('Package', null=True)

    class Meta:
        db_table = 'product2package'


# 套餐中包含的产品
class Package2Product(models.Model):
    product = models.ForeignKey('Products', )
    package = models.ForeignKey('Package', related_name='package2product')

    class Meta:
        db_table = 'package2product'


class Coupon(models.Model):
    name = models.CharField(max_length=60, verbose_name='优惠卷名称')
    price = models.IntegerField(verbose_name='金额')
    number = models.IntegerField(verbose_name='数量')
    activation = models.IntegerField(verbose_name='激活数量')
    use_number = models.IntegerField(verbose_name='使用数量')
    status = models.SmallIntegerField(verbose_name='状态')
    type = models.SmallIntegerField(verbose_name='类型')
    valid = models.SmallIntegerField(verbose_name='有效期')
    isExpired = models.SmallIntegerField(verbose_name='是否过期')
    ctime = models.DateTimeField(null=True, auto_now_add=True)
    employee = models.ForeignKey('Employees')
