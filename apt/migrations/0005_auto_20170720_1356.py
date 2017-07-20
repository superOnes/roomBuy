# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-20 05:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apt', '0004_eventdetail_sign'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventdetail',
            name='price',
        ),
        migrations.AlterField(
            model_name='eventdetail',
            name='floor',
            field=models.IntegerField(verbose_name='楼层'),
        ),
        migrations.AlterField(
            model_name='eventdetail',
            name='room_num',
            field=models.IntegerField(max_length=50, verbose_name='房号'),
        ),
    ]
