from django import forms
from django.forms import fields
from django.forms import widgets
from reposition import models


class BxsilderForm(forms.Form):
    """
    首页幻灯片上传
    """
    status = fields.CharField(
        widget=widgets.RadioSelect(choices=((1, '上架'), (0, '下架')))
    )
    img = fields.ImageField(
        required=True,
        error_messages={
            'required': '图片不能为空',
            'invalid': '文件类型上传错误',
        }
    )
    weight = fields.IntegerField(
        required=False,
        error_messages={
            'invalid': '请输入整数'
        }
    )

class BxsilderEditForm(forms.Form):
    status = fields.CharField(
        widget=widgets.RadioSelect(choices=((1, '上架'), (0, '下架')))
    )
    img = fields.ImageField(
        required=False,
        error_messages={
            'invalid': '文件类型上传错误',
        }
    )
    weight = fields.IntegerField(
        required=False,
        error_messages={
            'invalid': '请输入整数'
        }
    )