# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-19 02:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apt', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='inside_space',
        ),
        migrations.RemoveField(
            model_name='event',
            name='inside_space_price',
        ),
        migrations.RemoveField(
            model_name='event',
            name='login_msg',
        ),
        migrations.RemoveField(
            model_name='event',
            name='price',
        ),
        migrations.AlterField(
            model_name='event',
            name='test_price',
            field=models.BooleanField(default=False, verbose_name='是否显示公测房价'),
        ),
    ]
