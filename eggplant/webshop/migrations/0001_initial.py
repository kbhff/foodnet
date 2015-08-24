# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=70)),
                ('description', models.TextField()),
                ('category', models.CharField(max_length=10, null=True, choices=[('fee', 'fee'), ('food bag', 'food bag')])),
                ('price', models.DecimalField(default=0, max_digits=5, decimal_places=2)),
                ('stock', models.PositiveIntegerField(default=1)),
                ('tax', models.DecimalField(default=0, max_digits=5, decimal_places=2)),
                ('enabled', models.BooleanField(default=True)),
                ('image', models.ImageField(upload_to='products', null=True)),
            ],
        ),
    ]
