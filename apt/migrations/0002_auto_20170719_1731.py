# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-19 09:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apt', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventdetail',
            name='total',
        ),
        migrations.AlterField(
            model_name='eventdetail',
            name='price',
            field=models.CharField(max_length=100, verbose_name='单价'),
        ),
    ]