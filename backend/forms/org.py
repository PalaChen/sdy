from django.forms import ModelForm
from django import forms
from reposition import models


class PositionForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        for field_name in cls.base_fields:
            filed_obj = cls.base_fields[field_name]
            filed_obj.widget.attrs.update({'class': 'form-control'})
        return ModelForm.__new__(cls)

    class Meta:
        model = models.Position
        fields = "__all__"
        exclude = ['counts']


class Permission2Action2roleForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        for field_name in cls.base_fields:
            filed_obj = cls.base_fields[field_name]
            filed_obj.widget.attrs.update({'class': 'tb_checkbook tb2'})
        return ModelForm.__new__(cls)

    class Meta:
        model = models.Position
        fields = "__all__"
