from django.conf.urls import url
from backend import views

urlpatterns = [
    url(r'^login.html$', views.login.login),

    url(r'^site.html$', views.site.site_manage, name='site_manage'),
    url(r'^site/bxslider.html$', views.site.bxslider, name='bxslider'),
    url(r'^site/bxslider_add', views.site.bxslider_upload),
    url(r'^site/bxslider_edit', views.site.bxslider_edit),
    url(r'^site/bxslider_del/(\d+)', views.site.bxslider_del),
    url(r'^login.html', views.login.login, name='login'),

    url(r'^articles.html', views.articles.articles, name='articles_all'),
    url(r'^articles_search.html', views.articles.articles_search, name='articles_serach'),
    url(r'^articles_add.html', views.articles.article_add, name='articles_add'),
    url(r'^articles_edit/(\d+).html', views.articles.article_edit, name='articles_edit'),

    url(r'^keywords.html', views.articles.keywords, name='keyword_all'),
    url(r'^keyword_add.html', views.articles.keyword_add, name='keyword_add'),

    url(r'^category.html', views.articles.category, name='category_all'),
    url(r'^category_add.html', views.articles.category_add, name='category_add'),

    url(r'^product/category.html', views.product.p_category, name='p_category'),
    url(r'^product/service.html', views.product.p_service, name='p_service'),
    url(r'^product/service_add.html', views.product.p_service_add, name='p_service_add'),
    url(r'^product/service_edit/(\d+).html', views.product.p_service_edit, name='p_service_edit'),
    url(r'^product/service_del/(\d+).html', views.product.p_service_del, name='p_service_del'),
    url(r'^product/business.html', views.product.p_business, name='p_business'),
    url(r'^product/business/add.html', views.product.p_business_add, name='p_business_add'),
    url(r'^product/business/edit/(\d+).html', views.product.p_business_edit, name='p_business_edit'),
    url(r'^attribute.html', views.product.attribute, name='attribute_all'),

    url(r'^product.html', views.product.product, name='product_all'),
    url(r'^product_add.html', views.product.product_add, name='product_add'),
    url(r'^product_edit/(\d+).html', views.product.product_edit, name='product_edit'),
    url(r'^product_del/(\d+).html', views.product.product_del, name='product_del'),
    url(r'^product/image.html', views.product.product_image_upload, name='product_image'),

]
