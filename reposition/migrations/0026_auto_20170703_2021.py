# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-03 20:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reposition', '0025_auto_20170629_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrecommend',
            name='type',
            field=models.SmallIntegerField(choices=[(0, '主页查询'), (1, '用户推荐')], default=1, verbose_name='类型'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userrecommend',
            name='recommend',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reposition.Users'),
        ),
    ]