# Generated by Django 2.1.5 on 2019-09-04 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sequence', '0026_wusresult_fastq_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wuspool',
            name='num_of_lanes',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
