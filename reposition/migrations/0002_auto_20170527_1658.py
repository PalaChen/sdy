# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-27 16:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reposition', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messagessend',
            old_name='employee',
            new_name='employee_id',
        ),
        migrations.RenameField(
            model_name='messagessend',
            old_name='order',
            new_name='order_id',
        ),
    ]