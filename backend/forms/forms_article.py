from django import forms
from django.forms import fields
from django.forms import widgets

from reposition import models


class ArticleForm(forms.Form):
    category_id = fields.IntegerField(
        widget=widgets.Select(attrs={'class': 'form-control'})
    )
    title = fields.CharField(max_length=60, required=True,
                             error_messages={
                                 'required': '题目不能为空',
                                 'max_length': '题目长度不能超过60个汉字',
                             },
                             )

    status = fields.ChoiceField(choices=[(1, '公开'), (-1, '审核'), (0, '草稿')],
                                error_messages={'invalid': '非法选择'},
                                widget=widgets.Select(attrs={'class': 'form-control'})
                                )
    is_top = fields.ChoiceField(choices=[(0, '不置顶'), (1, '置顶')],
                                error_messages={'invalid': '非法选择'},
                                widget=widgets.Select(attrs={'class': 'form-control'}))

    content = fields.CharField(required=True,
                               error_messages={
                                   'required': '题目不能为空',
                               })
    keyword = fields.CharField(
        required=False
    )
    summary = fields.CharField(max_length=300, error_messages={'max_length': '摘要长度最多300个字',
                                                               'required': '摘要不能为空',})

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['category_id'].widget.choices = models.ArticlesCategory.objects.values_list('id', 'name')


class ArticleSearchForm(forms.Form):
    category_id = fields.IntegerField(
        widget=widgets.Select(attrs={'class': 'form-control'}),
        required=False
    )
    status = fields.ChoiceField(choices=[(1, '公开'), (-1, '审核'), (0, '草稿')],
                                required=False,
                                error_messages={'invalid': '非法选择'},
                                widget=widgets.Select(attrs={'class': 'form-control'})
                                )
    is_top = fields.ChoiceField(choices=[(0, '不置顶'), (1, '置顶')],
                                required=False,
                                error_messages={'invalid': '非法选择'},
                                widget=widgets.Select(attrs={'class': 'form-control'}))

    text = fields.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(ArticleSearchForm, self).__init__(*args, **kwargs)
        self.fields['category_id'].widget.choices = models.ArticlesCategory.objects.values_list('id', 'name')


class CategoryForm(forms.Form):
    name = fields.CharField(max_length=10, required=True, error_messages={'required': '分类名字不能为空',
                                                                          'max_length': '长度不能超过10个汉字',
                                                                          })
    sort = fields.IntegerField(
        required=False,
        error_messages={
            'invalid': '请输入数字',
        }
    )
    parent_id = fields.IntegerField(
        widget=widgets.Select(),
        error_messages={
            'required': '不能为空',
            'invalid': '非法数据,请重新输入',
        }
    )

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['parent_id'].widget.choices = models.ArticlesCategory.objects.values_list('id', 'name')


class KeywordForm(forms.Form):
    name = fields.CharField(
        error_messages={
            'required': '标签名不能为空'
        }
    )
