# Generated by Django 2.1.5 on 2019-09-10 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sequence', '0028_auto_20190910_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wussubmission',
            name='dual_barcode',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
