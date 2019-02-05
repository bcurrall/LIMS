# Generated by Django 2.1.5 on 2019-02-05 23:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('library', '0006_auto_20190205_1302'),
    ]

    operations = [
        migrations.CreateModel(
            name='WUSResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lane_id', models.IntegerField(blank=True, null=True)),
                ('barcode', models.CharField(blank=True, max_length=100, null=True)),
                ('counts', models.IntegerField(blank=True, null=True)),
                ('library_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='library.PoolingAmount')),
            ],
        ),
        migrations.CreateModel(
            name='WUSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('illumina_chemistry_ends', models.CharField(blank=True, max_length=100, null=True)),
                ('illumina_chemistry_length', models.IntegerField(blank=True, null=True)),
                ('dual_barcode', models.BooleanField(blank=True, choices=[(True, 'yes'), (False, 'no')], null=True)),
                ('barcode_size_bp', models.IntegerField(blank=True, null=True)),
                ('platform', models.CharField(blank=True, max_length=100, null=True)),
                ('requested_number_of_lanes', models.IntegerField(blank=True, null=True)),
                ('quote_number', models.CharField(blank=True, max_length=100, null=True)),
                ('submission_date', models.DateField(blank=True, null=True)),
                ('submitted_by', models.CharField(blank=True, max_length=100, null=True)),
                ('broad_id', models.CharField(blank=True, max_length=100, null=True)),
                ('walk_up_submission_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='library.PoolingAmount')),
            ],
        ),
    ]
