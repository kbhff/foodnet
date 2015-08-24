# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0003_auto_20150824_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False),
        ),
        migrations.AlterIndexTogether(
            name='basket',
            index_together=set([('user', 'status')]),
        ),
    ]
