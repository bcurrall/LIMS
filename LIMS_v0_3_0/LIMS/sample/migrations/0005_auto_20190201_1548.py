# Generated by Django 2.1.5 on 2019-02-01 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0004_auto_20190131_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='conc_nanodrop',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='sample',
            name='conc_qubit',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='sample',
            name='conc_tapestation',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='sample',
            name='rin_din_tapestation',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
