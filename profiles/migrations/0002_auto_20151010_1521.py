# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='address',
            field=models.ForeignKey(to='profiles.Address', null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='school',
            field=models.ForeignKey(to='profiles.School', null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='studies_domain',
            field=models.ForeignKey(to='profiles.StudiesDomain', null=True),
        ),
    ]
