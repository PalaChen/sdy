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
        validators=[RegexValidator(r'^[1][3578][0-9]{9}$', '请输入正确的手机号码')],
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


class codeForm(forms.Form):
    code = fields.CharField(required=True, error_messages={'required': '验证码不能为空'}
                            )


class BasicForm(forms.Form):
    phone = fields.IntegerField(
        required=True,
        validators=[RegexValidator(r'^[1][3578][0-9]{9}$', '请输入正确的手机号码')],
        error_messages={
            'required': '手机号码不能为空',
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
    verify_code = fields.IntegerField(required=True, error_messages={'required': '短信验证码不能为空',
                                                                     'invalid': '短信验证码输入有误',
                                                                     }
                                      )

    def clean(self):
        v1 = self.cleaned_data.get('password')
        v2 = self.cleaned_data.get('password2')

        if v1 != v2:
            raise ValidationError('密码输入不一致')


class GenerResiterForm(BasicForm):
    email = fields.EmailField(
        required=True,
        error_messages={
            'required': '邮箱不能为空',
            'invalid': '请输入正确的邮箱',
        }
    )
    name = fields.CharField(
        required=True,
        error_messages={'required': '姓名不能为空', }
    )


class RegisterForm(codeForm, GenerResiterForm):
    pass


class WapRegisterForm(GenerResiterForm):
    pass


class WapForgetPassForm(BasicForm):
    pass


class ForgetPassForm(BasicForm):
    code = fields.CharField(
        required=True,
        error_messages={
            'required': '验证码不能为空'
        }
    )


class UserConsultationForm(forms.Form):
    phone = fields.IntegerField(
        validators=[RegexValidator(r'^[1][3578][0-9]{9}$', '请输入正确的手机号码')],
        error_messages={
            'required': '手机号码不能为空',
            'invalid': '请输入正确的手机号码',
        }
    )
    remark = fields.CharField(max_length=200, error_messages={'required': '查询内容不能为空',
                                                              "max_length": '内容长度不能超过200个汉字',
                                                              }
                              )
    name = fields.CharField(max_length=100, error_messages={'required': '姓名不能为空',
                                                            "max_length": '姓名长度不能超过100个汉字',
                                                            }
                            )
