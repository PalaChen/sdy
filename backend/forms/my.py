from django.forms import ModelForm
from reposition import models


class OrderBusinessAddForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        return ModelForm.__new__(cls)

    class Meta:
        model = models.Process
        fields = ['order', 'process_name', 'step_name', 'employee', 'employee_name']
