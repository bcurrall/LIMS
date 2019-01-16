# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-03 19:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boxpos',
            name='box_pos',
        ),
        migrations.RemoveField(
            model_name='freezerpos',
            name='pos',
        ),
        migrations.AddField(
            model_name='boxpos',
            name='column',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='boxpos',
            name='row',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='freezerpos',
            name='column',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='freezerpos',
            name='rack',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='freezerpos',
            name='row',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='freezerpos',
            name='shelf',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='individual',
            name='project_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Project'),
        ),
    ]