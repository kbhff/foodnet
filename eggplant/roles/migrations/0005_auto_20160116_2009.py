# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0004_auto_20160116_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roleassignment',
            name='role',
            field=models.CharField(max_length=100, choices=[('purchaser', 'purchaser'), ('communicator', 'communicator'), ('packer', 'packer'), ('cashier', 'cashier'), ('accountant', 'accountant')]),
        ),
        migrations.AlterField(
            model_name='roleassignment',
            name='user',
            field=models.ForeignKey(related_name='role_assignments', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
