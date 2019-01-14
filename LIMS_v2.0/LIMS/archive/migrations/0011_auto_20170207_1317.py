# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-07 18:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0010_auto_20170207_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='freezer',
            name='columns',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='freezer',
            name='racks',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='freezer',
            name='rows',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='freezer',
            name='shelves',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='freezerpos',
            name='column',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='freezerpos',
            name='rack',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='freezerpos',
            name='row',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='freezerpos',
            name='shelf',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
