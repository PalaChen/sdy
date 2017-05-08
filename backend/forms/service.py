from django import forms
from django.forms import ModelForm, fields, widgets
from reposition import models
from django.db.models import Q


class OrderAddForm(forms.Form):
    product_id = fields.IntegerField(widget=widgets.Select(attrs={'class': 'form-control'}),
                                     error_messages={
                                         'required': '必须选择一个'
                                     })
    cprice = fields.FloatField(error_messages={'required': '价格不能为空'})
    number = fields.IntegerField(error_messages={'required': '数量不能为空'})
    order_state = fields.ChoiceField(choices=((0, '待付款'), (1, '待服务'), (2, '服务中'), (3, '服务完成')))
    name = fields.CharField(error_messages={'required': '姓名不能为空'})
    phone = fields.IntegerField(error_messages={'required': '手机号码不能为空'})
    payment = fields.ChoiceField(choices=((0, '支付宝'), (1, '微信'), (2, '线下支付'), (3, '网银支付')))


class AssignEmployeeForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        return ModelForm.__new__(cls)

    class Meta:
        model = models.MyTask
        fields = ['order', 'employee', 'order_serice']
