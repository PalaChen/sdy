from django.conf.urls import url
from wap import views

urlpatterns = [
    url(r'switch_city.html', views.index.switch_city, name='wap_switch_city'),
    url(r'commentlist.html', views.index.commentlist, name='wap_commentlist'),
    url(r'get_product/(\d+).html', views.index.getProduct, name='wap_getProduct'),
    url(r'product/(\d+).html', views.index.productinfo, name='wap_productinfo'),
    url(r'switch_product.html', views.index.switch_product, name='wap_switch_product'),
    url(r'selectset/(\d+).html', views.index.selectset, name='wap_selectset'),
    url(r'buy_pacakage.html', views.index.buy_pacakage, name='wap_buy_pacakage'),
    url(r'buy_product.html', views.index.buy_product, name='wap_buy_product'),
    url(r'serinfverify/(\d+).html', views.index.serinfverify, name='wap_serinfverify'),
    url(r'shopping.html', views.index.shopping, name='wap_shopping'),
    url(r'numofproduct.html', views.index.numOfProduct, name='wap_numOfProduct'),
    url(r'delproduct.html', views.index.delProduct, name='wap_delProduct'),
    url(r'buy.html', views.index.buy, name='wap_buy'),

    url(r'coupon.html', views.index.coupon, name='wap_coupon'),
    url(r'modeofpay/(\d+).html', views.index.modeofpay, name='wap_modeofpay'),
    url(r'order/topay/(\d+).html', views.index.order_topay, name='wap_orderToPay'),
    url(r'payment_method.html', views.index.payment_method, name='wap_payment_method'),
    url(r'alipay/return/', views.index.alipay_return_url, name='wap_alipay_return_url'),
    url(r'alipay/notify/', views.index.alipay_notify_url, name='wap_alipay_notify_url'),

    url(r'orderlist.html', views.index.orderlist, name='wap_orderlist'),
    url(r'cancelorders/(\d+).html', views.index.cancelorders, name='wap_cancelorders'),
    url(r'cancelrefund/(\d+).html', views.index.cancelRefund, name='wap_cancelRefund'),
    url(r'refund/(\d+).html', views.index.orderRefund, name='wap_orderRefund'),
    url(r'order_process/(\d+).html', views.index.orderProcess, name='orderProcess'),

    url(r'category.html', views.index.category, name='wap_category'),
    url(r'p_category/(\d+).html', views.index.p_category, name='wap_p_category'),
    url(r'findpass.html', views.index.findpass, name='wap_findpass'),
    url(r'mycenter.html', views.index.mycenter, name='wap_mycenter'),
    url(r'question.html', views.index.question, name='wap_question'),
    url(r'aboutus.html', views.index.aboutus, name='wap_aboutus'),

    url(r'myinvoice.html', views.index.mycenter, name='wap_myinvoice'),
    url(r'register.html', views.index.register, name='wap_register'),
    url(r'login.html', views.index.login, name='wap_login'),
    url(r'logout.html', views.index.logout, name='wap_logout'),
    url(r'city.html', views.index.city, name='wap_city'),

    url(r'', views.index.index, name='wap_index'),

]
