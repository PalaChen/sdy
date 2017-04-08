from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'login.html', views.account.login, name='login'),
    url(r'register.html', views.account.register, name='register'),
    url(r'get_captcha.html', views.account.get_captcha, name='get_captcha'),

    url(r'user$', views.user.index, name='user_index'),
    url(r'user/order.html', views.user.order, name='user_order'),

    url(r'user/order/(\d+).html$', views.user.order_query, name='order_query'),
    url(r'user/order_process/(\d+).html$', views.user.order_process_query),

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



    url(r'shop.html', views.pay.index, name='shopping_index'),

    # url(r'news/-(/d+)-(/d+).html', views.news.article, name='news_article'),




    url(r'', views.index.index, name='web_index'),

]
