# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0004_auto_20150824_0918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('weekly bag', 'weekly bag'), ('dry goods', 'dry goods'), ('loose weight vegetables', 'loose weight vegetables'), ('dairy', 'dairy'), ('fee', 'fee')], null=True, max_length=50),
        ),
    ]
