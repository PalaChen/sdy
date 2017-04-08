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
        # validators=[RegexValidator(r'^\d+${11}', '请输入数字')],
        error_messages={
            'required': '该字段不能为空',
            'invalid': '请输入手机号码',
        }
    )
    password = fields.CharField(
        required=True,
        min_length=7,
        error_messages={
            'min_length': '密码长度不能少于7位',
            'required': '该字段不能为空',
        }
    )


class RegisterForm(forms.Form):
    phone = fields.IntegerField(
        required=True,
        validators=[RegexValidator(r'^[1][358][0-9]{9}$', '请输入数字')],
        error_messages={
            'required': '该字段不能为空',
            'invalid': '请输入正确的手机号码',
        }
    )
    password = forms.RegexField(
        '^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
        required=True,
        min_length=7,
        max_length=32,
        error_messages={
            'required': '密码不能为空',
            'invalid': '密码必须包含数字，字母、特殊字符',
            'min_length': '密码不能少于7位',
            'max_length': '密码不能大于32位'
        }
    )

    password2 = forms.RegexField(
        '^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
        required=True,
        min_length=7,
        max_length=32,
        error_messages={
            'required': '密码不能为空',
            'invalid': '密码必须包含数字，字母、特殊字符',
            'min_length': '密码不能少于7位',
            'max_length': '密码不能大于32位'
        }
    )
    code = fields.CharField(
        required=True,
        error_messages={
            'required': '验证码不能为空'
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
