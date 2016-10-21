# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import eggplant.market.models.inventory
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to=eggplant.market.models.inventory.do_upload_product_image, null=True),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
