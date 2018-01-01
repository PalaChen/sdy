from django import forms
from django.forms import fields
from django.forms import widgets
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class EditProfileForm(forms.Form):
    email = fields.EmailField(error_messages={'required': '该字段不能为空',
                                              'invalid': '请输入正确的邮箱'
                                              })
    name = fields.CharField(max_length=10, error_messages={'required': '该字段不能为空',
                                                           'max_length': '最大长度不能超过10',
                                                           }
                            )
    address = fields.CharField(required=False)
    # province = fields.IntegerField(error_messages={'invalid': '选择错误'})
    # city = fields.IntegerField(error_messages={'invalid': '选择错误'})
    # area = fields.IntegerField(error_messages={'invalid': '选择错误'})
    know = fields.IntegerField(required=False, error_messages={'invalid': '选择错误'})


class EditPhoneForm(forms.Form):
    password = fields.CharField(
        error_messages={
            'required': '该字段不能为空',
        }
    )
    phone = fields.RegexField(
        '^[1][358][0-9]{9}$',
        required=True,
        error_messages={
            'required': '该字段不能为空',
            'invalid': '请输入正确的手机号码'
        }
    )
    verify_code = fields.IntegerField(
        max_value=9999,
        min_value=0000,
        error_messages={'invalid': '验证码输入有误',
                        'required': '请输入验证码',
                        'max_value': '验证码输入有误',
                        'min_value': '验证码输入有误',
                        })


class EditPwdForm(forms.Form):
    old_password = fields.CharField(
        required=True,
        min_length=7,
        max_length=32,
        error_messages={
            'required': '密码不能为空',
            'min_length': '密码不能少于7位',
            'max_length': '密码不能大于32位'
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
    paasword2 = forms.RegexField(
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

    def clean(self):
        v1 = self.cleaned_data.get('password')
        v2 = self.cleaned_data.get('password2')
        if v1 and v2:
            if v1 == v2:
                pass
            else:
                raise ValidationError('密码输入不一致')


class UserRecommendForm(forms.Form):
    name = fields.CharField(max_length=30, error_messages={
        'required': '该字段不能为空',
        'max_length': '最大长度不能超过30',
    })
    phone = fields.IntegerField(
        validators=[RegexValidator(r'^[1][3578][0-9]{9}$', '请输入正确的手机号码')],
        error_messages={'required': '手机号码不能为空',
                        'invalid': '请输入正确的手机号码',
                        })
    # business = fields.IntegerField(error_messages={'required': '业务类型不能为空',
    #                                                'invalid': '请正确勾选的业务类型', })
    # ctime = fields.DateField(error_messages={'invalid': '时间格式错误'})
    remark = fields.CharField(max_length=300, required=False)
    isknow = fields.IntegerField(required=False, error_messages={'invalid': '请勾选客户知晓您为其推荐', })
