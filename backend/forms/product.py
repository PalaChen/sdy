from django import forms
from django.forms import fields, widgets
from reposition import models
from django.db.models import Q

cate_obj = models.ProductCategory.objects.all()


def get_cate_tupe(cate_list):
    cate_tuple = {}
    for row in cate_list:
        if row.cate_rootid == 0 and row.cate_parentid == 0:
            cate_tuple.update({(row.id, row.cate_name): {}})
        elif row.cate_rootid != 0:
            for k in cate_tuple.keys():
                if k[0] == row.cate_rootid:
                    # print(cate_tuple[k])
                    cate_tuple[k].update({(row.id, '　|-' + row.cate_name): []})
        else:
            for k in cate_tuple.keys():
                for k1 in cate_tuple[k].keys():
                    if k1[0] == row.cate_parentid:
                        cate_tuple[k][k1].append((row.id, '　　|-' + row.cate_name))
    cate_tuple = str(cate_tuple).replace(':', ',')
    for i in ['{', '}', '[', ']']:
        cate_tuple = cate_tuple.replace(i, '')
    cate_tuple = cate_tuple.replace(', ,', ',')
    cate_tuple = list(eval(cate_tuple))
    return cate_tuple


class ProCategoryForm(forms.Form):
    cate_name = fields.CharField(max_length=10, error_messages={'required': '分类名称不能为空',
                                                                'max_length': '名字不能超过10个汉字',
                                                                })
    cate_sort = fields.IntegerField(required=False, error_messages={'max_length': '名字不能超过10个汉字',})
    cate_rootid = fields.IntegerField(
        widget=widgets.Select(attrs={'class': 'form-control'}),
        error_messages={
            'required': '必须选择一个'
        })

    def __init__(self, *args, **kwargs):
        super(ProCategoryForm, self).__init__(*args, **kwargs)
        self.fields['cate_rootid'].widget.choices = get_cate_tupe(cate_obj)


class ProServiceForm(forms.Form):
    name = fields.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': '服务名称不能为空'}
    )
    number = fields.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': '服务编号不能为空'}
    )
    renewal_reminder = fields.ChoiceField(
        choices=((0, '不提醒'), (1, '提醒'),),
        widget=widgets.RadioSelect(),
        error_messages={'required': '续费提醒不能为空'}

    )
    category_id = fields.IntegerField(
        widget=widgets.Select(attrs={'class': 'form-control'}),
        error_messages={
            'required': '必须选择一个'
        })

    def __init__(self, *args, **kwargs):
        super(ProServiceForm, self).__init__(*args, **kwargs)
        self.fields['category_id'].widget.choices = get_cate_tupe(cate_obj)


class ProBusinessForm(forms.Form):
    name = fields.CharField(max_length=30, error_messages={'required': '业务名称不能为空',
                                                           'max_length': '长度不能超过30个汉字',})
    step_number = fields.IntegerField(error_messages={'required': '业务名称不能为空',
                                                      'invalid': '请输入证书数字',})
    step_name = fields.CharField(max_length=30, error_messages={'required': '业务不能为空',
                                                                'max_length': '长度不能超过30个汉字',})


class ProductForm(forms.Form):
    p_name = fields.CharField(max_length=50,
                              error_messages={
                                  'required': '产品名称不能为空',
                                  'max_length': '长度不能超过50个汉字',
                              })
    p_category_id = fields.IntegerField(
        widget=widgets.Select(attrs={'class': 'form-control'}),
        error_messages={
            'required': '必须选择一个'})
    p_serivce_id = fields.IntegerField(
        widget=widgets.Select(attrs={'class': 'form-control'}),
        error_messages={'required': '必须选择一个'})

    p_business_id = fields.IntegerField(
        widget=widgets.Select(attrs={'class': 'form-control'}),
        error_messages={'required': '必须选择一个'})

    p_price = fields.FloatField(error_messages={'required': '价格不能为空',
                                                'invalid': '请输入数字'})


    p_market_price = fields.FloatField(required=False, error_messages={'invalid': '请输入数字'})
    p_seo_title = fields.CharField(required=False, max_length=80, error_messages={'max_length': '不能超过80个字符'})
    p_seo_keyword = fields.CharField(required=False, max_length=100, error_messages={'max_length': '不能超过100个字符'})
    p_seo_description = fields.CharField(required=False, max_length=300,
                                         error_messages={'max_length': '不能超过300个字符'})
    p_details = fields.CharField(required=True, error_messages={'required': '内容不能为空'})

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['p_category_id'].widget.choices = get_cate_tupe(cate_obj)
        self.fields['p_serivce_id'].widget.choices = models.ProductService.objects.values_list('id', 'name')
        self.fields['p_business_id'].widget.choices = models.ProcessName.objects.values_list('id', 'name')

class ProductImage(forms.Form):
    img = fields.ImageField(error_messages={'required': '上传图片',
                                            'invalid': '文件类型上传错误',})
