# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-07 17:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0008_auto_20170207_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individual',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Project'),
        ),
    ]
