# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-07 19:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reposition', '0016_auto_20170507_1949'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='area',
            new_name='city',
        ),
    ]