# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-06 16:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apt', '0016_eventdetail_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='housetype',
            name='num',
        ),
    ]
