# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-12 16:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reposition', '0035_productrecommend_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='parent_id',
            field=models.SmallIntegerField(db_column='cate_ParentID', default=0),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='root_id',
            field=models.SmallIntegerField(db_column='cate_RootID', default=0),
        ),
        migrations.AlterField(
            model_name='productrecommend',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '推荐'), (1, '下线')], default=0, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='products',
            name='p_putaway',
            field=models.SmallIntegerField(choices=[(0, '下架'), (1, '上架')], db_column='p_Putaway', default=1),
        ),
        migrations.AlterField(
            model_name='products',
            name='p_service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reposition.ProductService'),
        ),
        migrations.AlterField(
            model_name='products',
            name='p_top',
            field=models.SmallIntegerField(choices=[(0, '不推荐'), (1, '推荐')], db_column='p_Top', default=0),
        ),
    ]