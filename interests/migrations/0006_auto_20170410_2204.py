# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-11 05:04
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('interests', '0005_auto_20170407_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interest',
            name='last_refreshed',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 11, 5, 4, 13, 601040, tzinfo=utc)),
        ),
    ]
