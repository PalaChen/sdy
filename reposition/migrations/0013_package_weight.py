# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-16 15:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reposition', '0012_auto_20170615_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='weight',
            field=models.SmallIntegerField(default=0, verbose_name='权重'),
        ),
    ]