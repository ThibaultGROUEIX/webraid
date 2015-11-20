# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import gallery.models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_picture_album'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='slug',
            field=models.SlugField(default='aa', unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='aa', unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='picture',
            name='slug',
            field=models.SlugField(default='aa', unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='picture',
            name='image',
            field=models.ImageField(upload_to=gallery.models.get_image_path),
        ),
    ]
