from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'login.html', views.account.login, name='login'),
    url(r'login_ajax.html', views.account.login_ajax, ),
    url(r'logout.html', views.account.logout, name='logout'),
    url(r'register.html', views.account.register, name='register'),
    url(r'register_ajax.html', views.account.register_ajax, ),
    url(r'forgetpass.html', views.account.forgetpass, name='forgetpass'),
    url(r'get_captcha.html', views.account.get_captcha, name='get_captcha'),

    url(r'user$', views.user.index, name='user_index'),
    url(r'user/order.html', views.user.order, name='user_order'),
    url(r'user/order/topay/(\d+).html', views.user.order_topay, name='user_order_topay'),

    url(r'user/order/(\d+).html$', views.user.order_query, name='order_query'),
    url(r'user/order_process/(\d+).html$', views.user.order_process_query),
    url(r'user/orders/cancelorders.html$', views.user.cancelorders),

    url(r'user/info.html', views.user.info, name='user_info'),
    url(r'user/change_phone.html', views.user.edit_phone, name='user_edit_phone'),
    url(r'user/get_verify_code.html', views.user.send_verify_code),
    url(r'user/change_pwd.html', views.user.edit_pwd, name='user_edit_pwd'),

    url(r'user/message_unread.html', views.user.message_unread, name='user_message_unread'),
    url(r'user/message.html', views.user.message_read, name='user_message_read'),

    url(r'news.html', views.news.index, name='news_index'),
    url(r'news/category_(\d+).html', views.news.category, name='news_category'),
    url(r'news/author_(\d+).html', views.news.author, name='news_author'),
    url(r'news/(\d+)-(\d+).html', views.news.article, name='news_article'),

    url(r'product/(\d+).html', views.product.index, name='product_index'),
    url(r'pacakage/(\d+).html', views.product.pacakage_index, name='pacakage_index'),
    url(r'get_cat_product.html', views.product.get_cat_product, ),
    url(r'get_product.html', views.product.get_product, ),
    url(r'product_city.html', views.product.product_city),
    url(r'product/package/ppid/(\d+).html', views.product.product_package),
    url(r'product/buy.html', views.product.buy, name='product_buy'),

    url(r'get_city.html', views.product.get_city, ),
    url(r'get_town/(\d+).json', views.product.get_town, ),
    url(r'p_category/(\d+).html', views.product.p_c_index, name='p_category_index'),

    url(r'cart.html', views.pay.cart, name='shopping_cart'),
    url(r'cart_number.html', views.pay.cart_number, name='shopping_cart_number'),
    url(r'cart_del.html', views.pay.cart_del, name='shopping_cart_del'),

    url(r'buy_info.html', views.pay.buy_info, name='shopping_buy'),
    url(r'pay/(\d+).html', views.pay.pay, name='shopping_pay'),
    url(r'pay/success/(\d+).html', views.pay.pay_judgment, name='pay_judgment'),
    url(r'pay/pay_fail.html', views.pay.pay_fail),
    url(r'payment_method.html', views.pay.payment_method, name='payment_method'),

    url(r'alipay/return/', views.pay.alipay_return_url, name='alipay_return_url'),
    url(r'alipay/notify/', views.pay.alipay_notify_url, name='alipay_notify_url'),

    # url(r'news/-(/d+)-(/d+).html', views.news.article, name='news_article'),

    url('api/products/areas/(\d+)', views.api.get_area, ),

    url(r'switch_city/(\d+).html', views.index.switch_city, name='switch_city'),
    url(r'', views.index.index, name='web_index'),

]
