# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 03:21
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('interests', '0008_interest_last_refreshed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interest',
            name='last_refreshed',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 3, 3, 21, 23, 334127, tzinfo=utc)),
        ),
    ]