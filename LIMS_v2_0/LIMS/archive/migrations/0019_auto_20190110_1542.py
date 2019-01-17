# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2019-01-10 20:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0018_auto_20190110_1245'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sample2',
            old_name='name',
            new_name='aliquot_id',
        ),
        migrations.RenameField(
            model_name='sample2',
            old_name='project',
            new_name='genetic_array',
        ),
        migrations.AddField(
            model_name='sample2',
            name='aliquot_pos_column',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='aliquot_pos_row',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='box_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='box_type',
            field=models.CharField(blank=True, choices=[('box', 'box'), ('matrix_box', 'matrix_box'), ('plate', 'plate')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='brood',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='case_control',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='cell_line_id',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='cell_line_mutation',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='cell_line_type',
            field=models.CharField(blank=True, choices=[('LCL', 'LCL'), ('iPS', 'iPS'), ('NSC', 'NSC'), ('iNeurons', 'iNeurons'), ('fibroblast', 'fibroblast')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='cells',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='collected_by',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='collection_batch',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='conc',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='date_collected',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='date_of_birth',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='ethnicity',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='freezer_column',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='freezer_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='freezer_rack',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='freezer_row',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='freezer_shelf',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='freezer_type',
            field=models.CharField(blank=True, choices=[('-80', '-80'), ('LN2', 'LN2'), ('-20', '-20'), ('Fridge', 'Fridge')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='passage_number',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='race',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='sample_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='sample_type',
            field=models.CharField(blank=True, choices=[('DNA', 'DNA'), ('RNA', 'RNA'), ('Cells', 'Cells'), ('RNASeq_Lib', 'RNASeq_Lib'), ('liWGS_Lib', 'liWGS_Lib'), ('CAPSeq_Lib', 'CAPSeq_Lib'), ('RNACAPSeq_Lib', 'RNACAPSeq_Lib')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='source_tissue',
            field=models.CharField(blank=True, choices=[('brain', 'brain'), ('brain_hippocampus', 'brain_hippocampus'), ('brain_cortex', 'brain_cortex'), ('brain_cerebellum', 'brain_cerebellum'), ('blood', 'blood'), ('liver', 'liver'), ('adipose', 'adipose'), ('skin', 'skin')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='strain',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='study_model',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='vol',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='sample2',
            name='weight',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
