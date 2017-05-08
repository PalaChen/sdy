from django.conf.urls import url
from backend import views

urlpatterns = [
    url(r'^login.html$', views.login.login, name='admin_login'),
    url(r'^logout.html$', views.login.logout, name='admin_logout'),
    # 获取左侧菜单
    # url(r'^get_menu.html', views.login.get_menu,),

    # 我的工作台
    url(r'^my_task.html$', views.my.task, name='my_task'),
    # url(r'^my_task/order_process.html$', views.my.order_process, name='my_task_order_process'),
    url(r'^my_task/order_business/(\d+).html$', views.my.order_business, name='my_task_order_business'),
    url(r'^my_task/order_business_add.html$', views.my.order_business_add, name='my_task_order_business_add'),
    url(r'^my_client.html$', views.my.client, name='my_client'),
    url(r'^my_client_add.html$', views.my.client_add, name='my_client_add'),
    url(r'^my_client_edit/(\d+).html$', views.my.client_edit, name='my_client_edit'),
    # 服务管理
    url(r'^service/order.html', views.service.order, name='service_order'),
    url(r'^service/order_add.html', views.service.order_add, name='service_order_add'),
    url(r'^service/payment.html', views.service.payment, name='service_payment'),
    url(r'^service/manage.html', views.service.manage, name='service_manage'),
    url(r'^service/order_business/(\d+).html', views.service.order_business, name='service_order_business'),
    url(r'^service/assign_employee.html', views.service.assign_employee, name='service_assign_employee'),

    # 营销管理 用户管理
    url(r'^users.html$', views.users.user, name='users_all'),
    url(r'^users_add.html$', views.users.users_add, name='users_add'),
    url(r'^users_edit/(\d+).html$', views.users.users_edit, name='users_edit'),
    # url(r'^user/keyword.html$', views.users.keyword, name='users_keyword'),
    url(r'^user/recommend.html$', views.users.recommend, name='users_recommend'),

    # 　文章
    url(r'^articles.html', views.articles.articles, name='articles_all'),
    url(r'^articles/upload_image.html', views.articles.article_image, name='article_up_image'),
    url(r'^articles_search.html', views.articles.articles_search, name='articles_serach'),
    url(r'^articles_add.html', views.articles.article_add, name='articles_add'),
    url(r'^articles_edit/(\d+).html', views.articles.article_edit, name='articles_edit'),
    # 文章关键词
    url(r'^keywords.html', views.articles.keywords, name='keyword_all'),
    url(r'^keyword_add.html', views.articles.keyword_add, name='keyword_add'),
    url(r'^keyword_edit.html', views.articles.keyword_edit, name='keyword_edit'),
    url(r'^keyword_del/(\d+).html', views.articles.keyword_del, name='keyword_del'),
    # 文章分类
    url(r'^category.html', views.articles.category, name='category_all'),
    url(r'^category_add.html', views.articles.category_add, name='category_add'),
    url(r'^category_edit.html', views.articles.category_edit, name='category_edit'),
    url(r'^category_del/(\d+).html', views.articles.category_del, name='category_del'),

    # 产品管理
    url(r'^product/category.html', views.product.p_category, name='p_category'),
    url(r'^product/category_add.html', views.product.p_category_add, name='p_category_add'),
    url(r'^product/category_edit.html', views.product.p_category_edit, name='p_category_edit'),
    url(r'^product/category_del/(\d+).html', views.product.p_category_del, name='p_category_del'),
    url(r'^product/service.html', views.product.p_service, name='p_service'),
    url(r'^product/service_add.html', views.product.p_service_add, name='p_service_add'),
    url(r'^product/service_edit/(\d+).html', views.product.p_service_edit, name='p_service_edit'),
    url(r'^product/service_del/(\d+).html', views.product.p_service_del, name='p_service_del'),
    url(r'^product/business.html', views.product.p_business, name='p_business'),
    url(r'^product/business/add.html', views.product.p_business_add, name='p_business_add'),
    url(r'^product/business/edit/(\d+).html', views.product.p_business_edit, name='p_business_edit'),
    url(r'^product/attribute.html', views.product.attribute, name='attribute_all'),

    url(r'^product.html', views.product.product, name='product_all'),
    url(r'^product_add.html', views.product.product_add, name='product_add'),
    url(r'^get_city_info.html', views.product.get_city_info,),
    url(r'^product_edit/(\d+).html', views.product.product_edit, name='product_edit'),
    url(r'^product_del/(\d+).html', views.product.product_del, name='product_del'),
    url(r'^product/image.html', views.product.product_image_upload, name='product_image'),
    url(r'^product/upload_image.html', views.product.product_ck_image, name='product_ck_image'),

    # 系统配置
    url(r'^site.html$', views.site.site_manage, name='site_manage'),
    url(r'^site/bxslider.html$', views.site.bxslider, name='bxslider'),
    url(r'^site/bxslider_add', views.site.bxslider_upload),
    url(r'^site/bxslider_edit', views.site.bxslider_edit),
    url(r'^site/bxslider_del/(\d+).html', views.site.bxslider_del),
    url(r'^site/nav.html$', views.site.nav, name='nav_index'),
    url(r'^site/nav_add.html$', views.site.nav_add, name='nav_add_index'),
    url(r'^site/nav_edit.html$', views.site.nav_edit, name='nav_edit_index'),
    url(r'^site/nav_del/(\d+).html$', views.site.nav_del, name='nav_del_index'),
    # 系统机构
    url(r'org/position.html', views.organization.position_index, name='org_position'),
    url(r'org/position_add.html', views.organization.position_add, name='position_add'),
    url(r'org/position_edit/(\d+).html', views.organization.position_edit, name='position_edit'),
    url(r'org/deparment_add.html', views.organization.deparment_add, name='deparment_add'),
    url(r'org/deparment_edit.html', views.organization.deparment_edit, name='deparment_edit'),
    url(r'org/deparment_del.html', views.organization.deparment_del, name='deparment_del'),
    url(r'org/employees.html', views.organization.employees, name='org_employees'),
    url(r'org/employees_add.html', views.organization.employees_add, name='org_employees_add'),
    url(r'org/employees_edit/(\d+).html', views.organization.employees_edit, name='org_employees_edit'),
    url(r'org/assign/(\d+).html', views.organization.assign, name='org_assign'),
    url(r'org/bind_permission.html', views.organization.bind_permission),
    url(r'org/roles.html', views.organization.roles, name='organization_roles'),

    # 区域
    url(r'area.html', views.area.area_index, name='area_index'),
    url(r'area_add.html', views.area.area_add, name='area_add'),
    url(r'area/citys.html', views.area.area_citys,),
]
