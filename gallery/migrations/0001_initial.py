# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titre', models.CharField(max_length=100)),
                ('caption', models.TextField(null=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name=b"Date d'ajout")),
                ('contributeurs', models.ManyToManyField(related_name='contributor_album', to=settings.AUTH_USER_MODEL)),
                ('createur', models.ForeignKey(related_name='creator_album', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titre', models.CharField(max_length=100)),
                ('caption', models.TextField(null=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name=b"Date d'ajout")),
                ('contributeurs', models.ManyToManyField(related_name='contributor_category', to=settings.AUTH_USER_MODEL)),
                ('createur', models.ForeignKey(related_name='creator_category', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titre', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to=b'photo/')),
                ('caption', models.TextField(null=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name=b"Date d'ajout")),
                ('createur', models.ForeignKey(related_name='creator_picture', to=settings.AUTH_USER_MODEL)),
                ('personnages', models.ManyToManyField(related_name='characters', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
