# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webshop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=15, choices=[('open', 'open'), ('checked-out', 'checked-out')], default='open')),
                ('order', models.OneToOneField(null=True, to='payments.Order')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='BasketItem',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('basket', models.ForeignKey(to='webshop.Basket', related_name='items')),
                ('product', models.ForeignKey(to='webshop.Product')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='basketitem',
            unique_together=set([('basket', 'product')]),
        ),
        migrations.AlterIndexTogether(
            name='basket',
            index_together=set([('user', 'status')]),
        ),
    ]
