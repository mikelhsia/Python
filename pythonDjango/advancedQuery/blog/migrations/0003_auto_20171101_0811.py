# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 08:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20171101_0731'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='name',
            new_name='firstname',
        ),
        migrations.AddField(
            model_name='author',
            name='lastname',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]
