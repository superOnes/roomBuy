# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-13 07:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20170712_1630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='opentime',
        ),
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.DateTimeField(verbose_name='订单时间'),
        ),
    ]
