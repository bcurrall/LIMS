# Generated by Django 2.1.5 on 2019-02-04 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_auto_20190201_1811'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pool_name', models.CharField(max_length=100)),
                ('rel_proportion', models.CharField(max_length=100)),
                ('amount_of_library_used', models.FloatField(blank=True, default=0, null=True)),
                ('library_amount', models.CharField(blank=True, max_length=100, null=True)),
                ('tapestation_size_bp', models.IntegerField(blank=True, null=True)),
                ('tapestation_conc', models.FloatField(blank=True, null=True)),
                ('tapestation_molarity_nM', models.FloatField(blank=True, null=True)),
                ('qpcr_conc', models.FloatField(blank=True, null=True)),
                ('qubit_conc', models.FloatField(blank=True, null=True)),
                ('made_date', models.FloatField(blank=True, default=0, null=True)),
                ('made_by', models.TextField(blank=True, null=True)),
                ('library_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='library.Library')),
            ],
        ),
    ]