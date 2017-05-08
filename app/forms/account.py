from django import forms
from django.forms import fields
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    """
        登陆
    """
    phone = fields.IntegerField(
        required=True,
        validators=[RegexValidator(r'^[1][358][0-9]{9}$', '请输入正确的手机号码')],
        error_messages={
            'required': '手机号码不能为空',
            'invalid': '请输入正确的手机号码',
        }
    )
    password = fields.CharField(
        required=True,
        error_messages={
            'required': '密码不能为空',
        }
    )


class RegisterForm(forms.Form):
    phone = fields.IntegerField(
        required=True,
        validators=[RegexValidator(r'^[1][3578][0-9]{9}$', '请输入正确的手机号码')],
        error_messages={
            'required': '该字段不能为空',
            'invalid': '请输入正确的手机号码',
        }
    )
    password = forms.RegexField(
        '^(?=.*[0-9])(?=.*[a-zA-Z])[0-9a-zA-Z]{7,32}$',
        required=True,
        min_length=7,
        max_length=32,
        error_messages={
            'required': '密码不能为空',
            'invalid': '密码必须包含数字，字母',
            'min_length': '密码长度不能少于7位',
            'max_length': '密码长度不能大于32位'
        }
    )

    password2 = forms.RegexField(
        '^(?=.*[0-9])(?=.*[a-zA-Z])[0-9a-zA-Z]{7,32}$',
        required=True,
        min_length=7,
        max_length=32,
        error_messages={
            'required': '密码不能为空',
            'invalid': '密码必须包含数字，字母',
            'min_length': '密码长度不能少于7位',
            'max_length': '密码长度不能大于32位'
        }
    )
    code = fields.CharField(
        required=True,
        error_messages={
            'required': '验证码不能为空'
        }
    )
    verify_code = fields.IntegerField(
        required=True,
        error_messages={
            'required': '短信验证码不能为空',
            'invalid': '短信验证码输入有误',
        }
    )
    email = fields.EmailField(
        required=True,
        error_messages={
            'required': '邮箱不能为空',
            'invalid': '请输入正确的邮箱',
        }
    )
    name = fields.CharField(
        required=True,
        error_messages={'required': '姓名不能为空',}
    )

    def clean(self):

        v1 = self.cleaned_data.get('password')
        v2 = self.cleaned_data.get('password2')
        if v1 and v2:
            if v1 == v2:
                pass
            else:
                raise ValidationError('密码输入不一致')


class ForgetPassForm(forms.Form):
    phone = fields.IntegerField(
        required=True,
        validators=[RegexValidator(r'^[1][358][0-9]{9}$', '请输入正确的手机号码')],
        error_messages={
            'required': '该字段不能为空',
            'invalid': '请输入正确的手机号码',
        }
    )
    password = forms.RegexField(
        '^(?=.*[0-9])(?=.*[a-zA-Z])[0-9a-zA-Z]{7,32}$',
        required=True,
        min_length=7,
        max_length=32,
        error_messages={
            'required': '密码不能为空',
            'invalid': '密码必须包含数字，字母',
            'min_length': '密码长度不能少于7位',
            'max_length': '密码长度不能大于32位'
        }
    )

    password2 = forms.RegexField(
        '^(?=.*[0-9])(?=.*[a-zA-Z])[0-9a-zA-Z]{7,32}$',
        required=True,
        min_length=7,
        max_length=32,
        error_messages={
            'required': '密码不能为空',
            'invalid': '密码必须包含数字，字母',
            'min_length': '密码长度不能少于7位',
            'max_length': '密码长度不能大于32位'
        }
    )
    code = fields.CharField(
        required=True,
        error_messages={
            'required': '验证码不能为空'
        }
    )
    verify_code = fields.IntegerField(
        required=True,
        error_messages={
            'required': '短信验证码不能为空',
            'invalid': '短信验证码输入有误',
        }
    )

    def clean(self):

        v1 = self.cleaned_data.get('password')
        v2 = self.cleaned_data.get('password2')
        if v1 and v2:
            if v1 == v2:
                pass
            else:
                raise ValidationError('密码输入不一致')
