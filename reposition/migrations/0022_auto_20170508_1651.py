# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-08 16:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reposition', '0021_auto_20170508_1647'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='product2area',
            table='product_to_area',
        ),
    ]