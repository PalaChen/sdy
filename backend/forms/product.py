from django import forms
from django.forms import ModelForm
from django.forms import fields, widgets
from reposition import models
from django.db.models import Q


def get_cate_tupe(cate_list):
    cate_tuple = {}
    for row in cate_list:
        # 一级
        if row.root_id == 0 and row.parent_id == 0:
            cate_tuple.update({(row.id, row.name): {}})
        elif row.root_id != 0:
            for k in cate_tuple.keys():
                # 二级
                if k[0] == row.root_id:
                    # print(cate_tuple[k])
                    cate_tuple[k].update({(row.id, '　|-' + row.name): []})
                else:
                    for k1 in cate_tuple[k].keys():
                        # print(k,k1)
                        if k1[0] == row.parent_id:
                            cate_tuple[k][k1].append((row.id, '　　|-' + row.name))

    cate_tuple = str(cate_tuple).replace(':', ',')
    for i in ['{', '}', '[', ']']:
        cate_tuple = cate_tuple.replace(i, '')
    cate_tuple = cate_tuple.replace(', ,', ',')
    try:
        cate_tuple = list(eval(cate_tuple))
    except Exception as e:
        cate_tuple = []
    cate_tuple.insert(0, (0, '--------------------'))
    return cate_tuple


def get_cate_tupe1(cate_list):
    cate_tuple = {}
    for row in cate_list:
        if row.root_id == 0 and row.parent_id == 0:
            cate_tuple.update({(row.id, row.name): {}})
        elif row.root_id != 0:
            for k in cate_tuple.keys():
                if k[0] == row.root_id:
                    # print(cate_tuple[k])
                    cate_tuple[k].update({(row.id, '　|-' + row.name): []})
        else:
            for k in cate_tuple.keys():
                for k1 in cate_tuple[k].keys():
                    if k1[0] == row.parent_id:
                        cate_tuple[k][k1].append((row.id, '　　|-' + row.name))

    cate_tuple = str(cate_tuple).replace(':', ',')
    for i in ['{', '}', '[', ']']:
        cate_tuple = cate_tuple.replace(i, '')
    cate_tuple = cate_tuple.replace(', ,', ',')
    cate_tuple = list(eval(cate_tuple))
    cate_tuple.insert(0, ('', '--------------------'))
    return cate_tuple


class ProCategoryForm(forms.Form):
    name = fields.CharField(max_length=20, error_messages={'required': '分类名称不能为空',
                                                           'max_length': '名字不能超过20个汉字',
                                                           })
    sort = fields.IntegerField(required=False, error_messages={'required': '请输入数字', })
    root_id = fields.IntegerField(
        widget=widgets.Select(attrs={'class': 'form-control'}),
        required=False,
        # error_messages={
        #     'required': '必须选择一个'
        # }

    )

    def __init__(self, *args, **kwargs):
        super(ProCategoryForm, self).__init__(*args, **kwargs)
        cate_obj = models.ProductCategory.objects.all()
        self.fields['root_id'].widget.choices = get_cate_tupe1(cate_obj)


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

    root_id = fields.IntegerField(
        required=False,
        widget=widgets.Select(attrs={'class': 'form-control'}, ),
        error_messages={
            'invalid': '选择错误'
        })

    def __init__(self, *args, **kwargs):
        super(ProServiceForm, self).__init__(*args, **kwargs)
        # cate_obj = models.ProductCategory.objects.all()
        # self.fields['category_id'].widget.choices = models.ProductService.objects.values_list('id', 'name')


class ProBusinessForm(forms.Form):
    name = fields.CharField(max_length=30, error_messages={'required': '业务名称不能为空',
                                                           'max_length': '长度不能超过30个汉字', })
    step_number = fields.IntegerField(error_messages={'required': '业务名称不能为空',
                                                      'invalid': '请输入数字', })
    step_name = fields.CharField(max_length=30, error_messages={'required': '业务不能为空',
                                                                'max_length': '长度不能超过30个汉字', })

class CityFrom(forms.Form):
    city_code = fields.IntegerField(error_messages={'required': '城市必须选择一个',
                                                    'invalid': '无效选择'})
    area_code = fields.IntegerField(error_messages={'required': '地区必须选择一个',
                                                    'invalid': '无效选择'})

class ProductForm(forms.Form):
    p_name = fields.CharField(max_length=50,
                              error_messages={
                                  'required': '产品名称不能为空',
                                  'max_length': '长度不能超过50个汉字',
                              })
    p_t_imgae = fields.CharField(error_messages={'required': '请上传图片', })
    p_category_id = fields.IntegerField(required=False,
                                        widget=widgets.Select(attrs={'class': 'form-control'}),
                                        error_messages={'invalid': '无效选择'})
    p_service_id = fields.IntegerField(required=False,
                                       widget=widgets.Select(attrs={'class': 'form-control'}, ),
                                       error_messages={'required': '服务类型必须选择一个',
                                                       'invalid': '无效选择'
                                                       })
    p_putaway = fields.ChoiceField(choices=((1, '上架'), (0, '下架')),
                                   widget=widgets.Select(attrs={'class': 'form-control'}),
                                   error_messages={'invalid': '无效选择'})
    p_top = fields.ChoiceField(choices=((0, '不推荐'), (1, '推荐')),
                               widget=widgets.Select(attrs={'class': 'form-control'}),
                               error_messages={'invalid': '无效选择'})
    p_business_id = fields.IntegerField(error_messages={'required': '业务类型必须选择一个',
                                                        'invalid': '无效选择'})

    p_price = fields.FloatField(error_messages={'required': '价格不能为空',
                                                'invalid': '请输入数字'})

    p_market_price = fields.FloatField(required=False, error_messages={'invalid': '请输入数字'})
    p_seo_keyword = fields.CharField(required=False, max_length=100, error_messages={'max_length': '不能超过100个字符'})
    p_seo_description = fields.CharField(required=False, max_length=300,
                                         error_messages={'max_length': '不能超过300个字符'})
    p_details = fields.CharField(error_messages={'required': '产品内容内容不能为空'})

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        cate_obj = models.ProductCategory.objects.all()
        self.fields['p_category_id'].widget.choices = get_cate_tupe(cate_obj)
        self.fields['p_service_id'].widget.choices = models.ProductService.objects.values_list('id', 'name')
        # self.fields['p_business_id'].widget.choices = models.ProcessName.objects.values_list('id', 'name')


class ProductAddForm(ProductForm,CityFrom):
    pass

class ProductEditForm(ProductForm):
    pass



class ImageForm(forms.Form):
    imgFile = fields.ImageField(error_messages={'required': '图片不能为空',
                                                'invalid': '文件类型上传错误', })


class PackageAdd(forms.Form):
    cover_image_id = fields.IntegerField(error_messages={'required': '请上传图片',
                                                         'invalid': '请上传图片', })
    weight = fields.IntegerField(error_messages={'required': '请输入数字',
                                                 'invalid': '请输入数字', })
    name = fields.CharField(max_length=64, error_messages={'required': '套餐名不能为空',
                                                           'max_length': '套餐名最大长度为64个汉字'})
    status = fields.IntegerField(error_messages={'invalid': '非法选择'}, )
    dscription = fields.CharField(widget=forms.Textarea, error_messages={'required': '套餐描述不能为空', })
    cprice = fields.FloatField(error_messages={'required': '套餐价格不能为空',
                                               'invalid': '套餐价格必须为数字'})
    original_price = fields.FloatField(error_messages={'required': '套餐原价格不能为空',
                                                       'invalid': '套餐原价格必须为数字'})
    area_id = fields.IntegerField(error_messages={'required': '非法输入,请重新创建套餐',
                                                  'invalid': '非法输入,请重新创建套餐'})


class PackageBind(forms.Form):
    package_id = fields.IntegerField(error_messages={'required': '套餐ID不能为空',
                                                     'invalid': '套餐ID必须为数字'})
    # product_id = fields.IntegerField(error_messages={'required': '必须选择一个产品',
    #                                                  'invalid': '非法选择'})


class ConponForm(forms.Form):
    name = fields.CharField(max_length=60, error_messages={'required': '优惠卷名称不能为空',
                                                           'max_length': '优惠卷名称最长不能超过50'})
    type = fields.IntegerField(error_messages={'required': '优惠卷类型不能为空',
                                               'invalid': '请输入数字'})
    status = fields.IntegerField(error_messages={'required': '必须选择优惠卷状态',
                                                 'invalid': '优惠卷状态非法选择'})
    price = fields.IntegerField(error_messages={'required': '优惠卷金额不能为空',
                                                'invalid': '优惠卷金额必须是整数'})
    # threshold = fields.IntegerField(error_messages={'required': '优惠卷使用门槛不能为空',
    #                                                 'invalid': '优惠卷使用门槛必须为整数'})
    number = fields.IntegerField(error_messages={'required': '优惠卷数量不能为空',
                                                 'invalid': '优惠卷数量必须为整数'})
    start_time = fields.DateTimeField(error_messages={'required': '开始时间不能为空',
                                                      'invalid': '开始时间必须为时间格式'})
    end_time = fields.DateTimeField(error_messages={'required': '结束时间不能为空',
                                                    'invalid': '结束时间必须为时间格式'})
    price_reduction = fields.IntegerField(required=False, error_messages={'required': '开始时间不能为空',
                                                                          'invalid': '开始时间必须为时间格式'})
