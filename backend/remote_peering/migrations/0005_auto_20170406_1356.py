# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-06 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remote_peering', '0004_auto_20170406_0826'),
    ]

    operations = [
        migrations.AddField(
            model_name='ip',
            name='num_paths',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='ip',
            name='num_peerings',
            field=models.IntegerField(null=True),
        ),
    ]
