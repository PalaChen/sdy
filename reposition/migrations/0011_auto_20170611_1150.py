# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-11 11:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reposition', '0010_remove_articlescoverimage_ul_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='cover_picture',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reposition.ProductTImage', verbose_name='封面图'),
        ),
        migrations.AlterField(
            model_name='package2product',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='package2product', to='reposition.Package'),
        ),
    ]
