# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-02 08:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('interests', '0014_auto_20170402_0121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interest',
            name='last_refreshed',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 2, 8, 27, 48, 695914, tzinfo=utc)),
        ),
    ]
