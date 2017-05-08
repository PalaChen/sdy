from django.conf.urls import url
from cxmadmin import views

urlpatterns = [
    url(r'^(\w+)/(\w+)/(\d+)/delete/$', views.table_obj_delete, name="obj_delete"),
    url(r'^(\w+)/(\w+)/(\d+)/change/$', views.table_obj_change, name="table_obj_change"),
    url(r'^(\w+)/(\w+)/add/$', views.table_obj_add, name="table_obj_add"),
    url(r'^(\w+)/(\w+)/$', views.table_obj_list, name="table_obj_list"),
    url(r'^login.html', views.admin_login),
    url(r'^logout/', views.admin_logout, ),
    url(r'^$', views.app_index, name="app_index"),
]
