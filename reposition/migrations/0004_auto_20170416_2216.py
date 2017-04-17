# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-16 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reposition', '0003_auto_20170416_2211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='payment',
        ),
        migrations.AlterField(
            model_name='orderpayment',
            name='payment',
            field=models.CharField(choices=[(0, '支付宝'), (1, '微信'), (2, '线下支付'), (3, '网银支付')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='orderpayment',
            name='status',
            field=models.IntegerField(choices=[(0, '待支付'), (1, '支付成功'), (2, '支付失败')], default=0),
        ),
    ]