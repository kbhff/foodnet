# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-12 13:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0006_merge'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='basketitem',
            unique_together=set([('basket', 'product', 'delivery_date')]),
        ),
    ]
