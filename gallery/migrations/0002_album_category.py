# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='category',
            field=models.ForeignKey(default=0, to='gallery.Category'),
            preserve_default=False,
        ),
    ]
