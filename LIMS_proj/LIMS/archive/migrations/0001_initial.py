# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-03 16:50
from __future__ import unicode_literals

import archive.models
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
            name='Box',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('box_type', models.CharField(blank=True, choices=[('9x9', '9x9'), ('10x10', '10x10'), ('96_plate', '96_plate'), ('96_matrix', '96_matrix')], max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BoxHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('history_type', models.CharField(blank=True, choices=[('Made', 'Made'), ('Moved', 'Moved'), ('Deleted', 'Deleted')], max_length=20, null=True)),
                ('timestamp', models.DateTimeField(default=archive.models.default_start_time)),
                ('box_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='archive.Box')),
            ],
        ),
        migrations.CreateModel(
            name='BoxPos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('box_pos', models.CharField(blank=True, max_length=50, null=True)),
                ('box_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='archive.Box')),
            ],
        ),
        migrations.CreateModel(
            name='FreezerPos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('freezer_type', models.CharField(blank=True, choices=[('-80', '-80'), ('LN2', 'LN2'), ('-20', '-20'), ('Fridge', 'Fridge')], max_length=20, null=True)),
                ('pos', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Individual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('alt_name1', models.CharField(blank=True, max_length=100, null=True)),
                ('alt_name2', models.CharField(blank=True, max_length=100, null=True)),
                ('project_id', models.CharField(choices=[('DGAP', 'DGAP'), ('SFARI', 'SFARI'), ('16p', '16p')], max_length=100)),
                ('species', models.CharField(blank=True, choices=[('Homo_sapiens', 'Homo_sapiens'), ('Mus_musculus', 'Mus_musculus')], max_length=100, null=True)),
                ('family_id', models.CharField(max_length=100)),
                ('relationship', models.CharField(max_length=30)),
                ('karyotype', models.CharField(blank=True, max_length=100, null=True)),
                ('other_genetic_info', models.CharField(blank=True, max_length=200, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Unknown', 'Unknown')], max_length=10, null=True)),
                ('year_of_birth', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_name', models.CharField(max_length=100)),
                ('tube_name', models.CharField(blank=True, max_length=100, null=True)),
                ('type', models.CharField(blank=True, choices=[('DNA', 'DNA'), ('RNA', 'RNA'), ('Cells', 'Cells'), ('RNASeq_Lib', 'RNASeq_Lib'), ('liWGS_Lib', 'liWGS_Lib'), ('CAPSeq_Lib', 'CAPSeq_Lib'), ('RNACAPSeq_Lib', 'RNACAPSeq_Lib')], max_length=100, null=True)),
                ('o_tissue', models.CharField(blank=True, choices=[('LCL', 'LCL'), ('iPS', 'iPS'), ('NSC', 'NSC'), ('iNeurons', 'iNeurons'), ('brain', 'brain'), ('blood', 'blood')], max_length=100, null=True)),
                ('parent_id', models.CharField(blank=True, max_length=100, null=True)),
                ('conc', models.FloatField(default=0)),
                ('vol', models.FloatField(default=0)),
                ('weight', models.FloatField(default=0)),
                ('cells', models.FloatField(default=0)),
                ('active', models.BooleanField(default=False)),
                ('box_pos', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='archive.BoxPos')),
                ('individual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='archive.Individual')),
            ],
        ),
        migrations.CreateModel(
            name='SampleHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(blank=True, choices=[('Entered', 'Entered'), ('Received', 'Received'), ('Moved', 'Moved'), ('Nanodrop', 'Nanodrop'), ('TapeStation', 'TapeStation'), ('Pico', 'Pico'), ('Weighed', 'Weighed')], max_length=100, null=True)),
                ('prev_conc', models.FloatField(default=0)),
                ('prev_vol', models.FloatField(default=0)),
                ('prev_weight', models.FloatField(default=0)),
                ('prev_cells', models.FloatField(default=0)),
                ('timestamp', models.DateTimeField(default=archive.models.default_start_time)),
                ('prev_box_pos', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='archive.BoxPos')),
                ('prev_freezer_pos', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='archive.FreezerPos')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='archive.Sample')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='boxhistory',
            name='prev_freezer_pos',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='archive.FreezerPos'),
        ),
        migrations.AddField(
            model_name='boxhistory',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='box',
            name='freezer_pos',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='archive.FreezerPos'),
        ),
    ]