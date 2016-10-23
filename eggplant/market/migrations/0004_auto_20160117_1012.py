# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0003_auto_20151112_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basketitem',
            name='delivery_date',
            field=models.DateField(null=True, default=django.utils.timezone.now),
        ),
    ]
