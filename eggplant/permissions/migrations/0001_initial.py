# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_account_department'),
        ('departments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='name', help_text='Human readable name, not used for any lookups so can be anything', max_length=64)),
                ('all_permissions', models.BooleanField(verbose_name='all permissions', default=False, help_text='Grant all permissions')),
                ('can_add_user_profiles', models.BooleanField(verbose_name='add users', default=False, help_text='Can add users to associated account or department, meaning that setting this value is only meaningful if an account or department is associated.')),
                ('can_change_account', models.BooleanField(verbose_name='change account(s)', default=False, help_text="Can change associated accounts' data. If associated to a department, gives global access to change all the accounts. If associated to an account, only gives access to that account.")),
            ],
        ),
        migrations.CreateModel(
            name='UserProfilePermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('is_global', models.BooleanField(verbose_name='global', default=False, help_text='This permission gives access across all departments')),
                ('account', models.ForeignKey(to='accounts.Account')),
                ('department', models.ForeignKey(to='departments.Department')),
                ('permission', models.ForeignKey(to='permissions.Permission')),
            ],
        ),
    ]
