# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=400)),
                ('description', models.CharField(default='', max_length=400)),
                ('start', models.DateTimeField(blank=True, verbose_name='Start')),
                ('end', models.DateTimeField(blank=True, verbose_name='End')),
                ('queueNo', models.IntegerField(default=0)),
                ('group', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=400)),
                ('type', models.CharField(choices=[('gym ', 'GYM'), ('football field', 'FOOTBALL FIELD'), ('volleyball grounds', 'VOLLEYBALL GROUNDS')], default='gym', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.CharField(max_length=3)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.Booking')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.Location'),
        ),
        migrations.AddField(
            model_name='booking',
            name='person',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
