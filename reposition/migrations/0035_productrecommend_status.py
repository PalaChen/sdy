# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-11 18:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reposition', '0034_auto_20170511_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='productrecommend',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '推荐'), (1, '下线')], default=1),
            preserve_default=False,
        ),
    ]
