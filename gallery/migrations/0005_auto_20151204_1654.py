# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import gallery.models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0004_auto_20151120_1831'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.ImageField(upload_to=b'gallery/%Y/%m/%d')),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='coverImage',
            field=models.ImageField(default=b'/home/ostrogrox/PycharmProjects/webraid/media/default/default.png', upload_to=gallery.models.get_album_coverImage_path),
        ),
        migrations.AddField(
            model_name='category',
            name='coverImage',
            field=models.ImageField(default=b'/home/ostrogrox/PycharmProjects/webraid/media/default/default.png', upload_to=gallery.models.get_category_coverImage_path),
        ),
    ]
