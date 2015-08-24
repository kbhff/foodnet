# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0002_auto_20150820_1144'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='basket',
            index_together=set([]),
        ),
    ]
