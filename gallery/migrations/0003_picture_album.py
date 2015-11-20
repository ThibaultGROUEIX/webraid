# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_album_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='album',
            field=models.ForeignKey(default=0, to='gallery.Album'),
            preserve_default=False,
        ),
    ]
