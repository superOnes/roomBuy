# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-15 17:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backstage', '0001_initial'),
        ('accounts', '0008_auto_20170815_1700'),
        ('apt', '0019_auto_20170807_1040'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='昵称')),
                ('house_limit', models.IntegerField(default=0, verbose_name='房源数量限制')),
                ('expire_date', models.DateTimeField(blank=True, null=True, verbose_name='账号过期日期')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backstage.City')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backstage.Province')),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apt.Client'),
        ),
        migrations.DeleteModel(
            name='Company',
        ),
    ]
