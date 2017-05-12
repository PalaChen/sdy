# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-10 18:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reposition', '0031_auto_20170510_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderpayment',
            name='total_price',
            field=models.FloatField(verbose_name='总价格'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='area',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='city',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
