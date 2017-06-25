# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-18 22:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reposition', '0014_auto_20170618_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='end_time',
            field=models.DateField(null=True, verbose_name='结束时间'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='isExpired',
            field=models.SmallIntegerField(choices=[(0, '已过期'), (1, '未过期')], default=1, verbose_name='是否过期'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='start_time',
            field=models.DateField(null=True, verbose_name='开始时间'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '冻结'), (1, '正常')], default=1, verbose_name='状态'),
        ),
    ]