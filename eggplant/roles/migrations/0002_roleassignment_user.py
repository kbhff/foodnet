# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('roles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='roleassignment',
            name='user',
            field=models.ForeignKey(verbose_name='user', editable=False, default=None, to=settings.AUTH_USER_MODEL, related_name='roles'),
            preserve_default=False,
        ),
    ]
