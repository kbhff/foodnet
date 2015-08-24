# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0005_auto_20150824_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='basketitem',
            name='delivery_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
