# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('middle_name', models.CharField(verbose_name='middle name', blank=True, help_text='Optional.', max_length=30)),
                ('address', models.CharField(max_length=255)),
                ('postcode', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=50)),
                ('tel', models.CharField(max_length=15)),
                ('tel2', models.CharField(null=True, max_length=15)),
                ('sex', models.CharField(max_length=100, choices=[('', '-----'), ('female', 'female'), ('male', 'male'), ('other', 'other')], null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('changed', models.DateTimeField(auto_now=True)),
                ('permissions', models.ManyToManyField(verbose_name='permissions', to='permissions.Permission', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='profile', verbose_name='user', editable=False)),
            ],
        ),
    ]
