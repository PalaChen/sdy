# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-13 22:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reposition', '0032_productspackages_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='productspackages',
            name='sort',
            field=models.SmallIntegerField(default=1, verbose_name='排序'),
            preserve_default=False,
        ),
    ]