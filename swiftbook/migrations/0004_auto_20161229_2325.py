# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-29 22:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swiftbook', '0003_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='gallery',
            field=models.ImageField(blank=True, null=True, upload_to=b'archivos', verbose_name=b'Imagen'),
        ),
    ]
