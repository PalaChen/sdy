# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-10 18:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reposition', '0030_auto_20170510_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderserice',
            name='area',
            field=models.CharField(default=1, max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderserice',
            name='city',
            field=models.CharField(default=1, max_length=64),
            preserve_default=False,
        ),
    ]
