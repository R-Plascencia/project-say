# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-27 06:31
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('interests', '0012_auto_20170326_0115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interest',
            name='keywords',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='interest',
            name='last_refreshed',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 27, 6, 31, 4, 557620, tzinfo=utc)),
        ),
    ]
