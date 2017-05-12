# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-11 09:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reposition', '0032_auto_20170510_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderserice',
            name='area',
            field=models.CharField(max_length=64, verbose_name='地区'),
        ),
        migrations.AlterField(
            model_name='orderserice',
            name='city',
            field=models.CharField(max_length=64, verbose_name='城市'),
        ),
        migrations.AlterField(
            model_name='products',
            name='p_service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reposition.ProductService'),
        ),
    ]
