from django.forms import ModelForm


# class UserForm(ModelForm):
#     class Meta:
#         model = models.Users
#         fields = ['name', 'phone', ]
#         # 显示所有字段
#         # fields = '__all__'
#
#     def __new(user,*arg,**kwargs):
#         print('__new__',user,arg,kwargs)

# 动态的生成modelform
def create_dynamic_model_form(admin_class, form_add=False):
    # 传入admin_class 是因为里面有类
    """
    动态的生成modelform
    :param admin_class:
    :param form_add: False 默认是修改的表单,True时为添加
    :return:
    """

    class Meta:
        model = admin_class.model
        fields = '__all__'
        if not form_add:
            # 获取不允许修改的字段
            exclude = admin_class.readonly_fields
            """
            admin_class从django项目启动到结束，都是同一个实例。
            为了避免上一次添加数据时，admin_class.form_add的值改为True。
            所以这里把form_add更改为fasle
            """
            admin_class.form_add = False
        else:
            admin_class.form_add = True

    def __new__(cls, *args, **kwargs):
        # 使用__new__方法获取动态类的所有字段
        # print('cls', cls)
        for field_name in cls.base_fields:
            filed_obj = cls.base_fields[field_name]
            filed_obj.widget.attrs.update({'class': 'form-control'})
        return ModelForm.__new__(cls)

    dynamic_form = type("DynamicModelForm", (ModelForm,), {'Meta': Meta, '__new__': __new__})
    return dynamic_form
