# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-29 22:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swiftbook', '0004_auto_20161229_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='gallery',
            field=models.ImageField(upload_to=b'swiftbook/images', verbose_name=b'image'),
        ),
    ]