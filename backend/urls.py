from django.conf.urls import url
from backend import views

urlpatterns = [
    url(r'^login.html$', views.login.login, name='admin_login'),
    url(r'^logout.html$', views.login.logout, name='admin_logout'),

    url(r'^my_task.html$', views.my.my_task, name='my_task'),
    url(r'^my_client.html$', views.my.my_client, name='my_client'),
    url(r'^site.html$', views.site.site_manage, name='site_manage'),
    url(r'^site/bxslider.html$', views.site.bxslider, name='bxslider'),
    url(r'^site/bxslider_add', views.site.bxslider_upload),
    url(r'^site/bxslider_edit', views.site.bxslider_edit),
    url(r'^site/bxslider_del/(\d+).html', views.site.bxslider_del),
    url(r'^site/nav.html$', views.site.nav, name='nav_index'),
    url(r'^site/nav_add.html$', views.site.nav_add, name='nav_add_index'),
    url(r'^site/nav_edit.html$', views.site.nav_edit, name='nav_edit_index'),
    url(r'^site/nav_del/(\d+).html$', views.site.nav_del, name='nav_del_index'),

    url(r'organization.html', views.organization.index, name='organization_index'),
    url(r'organization/bind_permission.html', views.organization.bind_permission, name='organization_index'),
    url(r'organization/assign/(\d+).html', views.organization.assign, name='organization_assign'),
    url(r'organization/roles.html', views.organization.roles, name='organization_roles'),
    url(r'organization/departments.html', views.organization.departments, name='organization_departments'),
    url(r'organization/employees.html', views.organization.employees, name='organization_employees'),

    url(r'^articles.html', views.articles.articles, name='articles_all'),
    url(r'^articles/upload_image.html', views.articles.article_image, name='article_up_image'),
    url(r'^articles_search.html', views.articles.articles_search, name='articles_serach'),
    url(r'^articles_add.html', views.articles.article_add, name='articles_add'),
    url(r'^articles_edit/(\d+).html', views.articles.article_edit, name='articles_edit'),

    url(r'^keywords.html', views.articles.keywords, name='keyword_all'),
    url(r'^keyword_add.html', views.articles.keyword_add, name='keyword_add'),
    url(r'^keyword_del/(\d+).html', views.articles.keyword_del, name='keyword_del'),

    url(r'^category.html', views.articles.category, name='category_all'),
    url(r'^category_add.html', views.articles.category_add, name='category_add'),
    url(r'^category_del/(\d+).html', views.articles.category_del, name='category_del'),

    url(r'^service/manage.html', views.service.manage, name='service_manage'),
    url(r'^service/order.html', views.service.order, name='service_order'),
    url(r'^service/order_add.html', views.service.order_add, name='service_order_add'),

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
    url(r'^product_edit/(\d+).html', views.product.product_edit, name='product_edit'),
    url(r'^product_del/(\d+).html', views.product.product_del, name='product_del'),
    url(r'^product/image.html', views.product.product_image_upload, name='product_image'),
    url(r'^product/upload_image.html', views.product.product_ck_image, name='product_ck_image'),

]
