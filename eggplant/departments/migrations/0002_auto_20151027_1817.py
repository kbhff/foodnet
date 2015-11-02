# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('sites', '0001_initial'),
        ('departments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='departmentadministrator',
            name='profile',
            field=models.ForeignKey(related_name='administrator_for', to='profiles.UserProfile'),
        ),
        migrations.AddField(
            model_name='department',
            name='site',
            field=models.ForeignKey(default=1, to='sites.Site'),
        ),
    ]
