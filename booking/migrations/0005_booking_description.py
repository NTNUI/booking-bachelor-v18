# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-19 17:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_booking_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='description',
            field=models.CharField(default='', max_length=400),
        ),
    ]
