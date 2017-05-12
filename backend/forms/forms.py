from django import forms
from django.forms import fields
from django.forms import widgets
from reposition import models


class LoginForm(forms.Form):
    """
        登陆
    """
    email = fields.EmailField(
        error_messages={
            'required': '邮箱不能为空',
            'invalid': '请输入正确的邮箱格式',
        }
    )
    password = fields.CharField(
        error_messages={
            'required': '密码不能为空',
        }
    )




