# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-09 15:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reposition', '0025_auto_20170509_1503'),
    ]

    operations = [
        migrations.RenameField(
            model_name='regionalmanagement',
            old_name='rid',
            new_name='r_code',
        ),
    ]
