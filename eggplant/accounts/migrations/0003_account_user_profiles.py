# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_account_department'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='user_profiles',
            field=models.ManyToManyField(to='profiles.UserProfile', related_name='accounts'),
        ),
    ]
