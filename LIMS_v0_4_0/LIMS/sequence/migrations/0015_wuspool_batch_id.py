# Generated by Django 2.1.5 on 2019-08-26 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sequence', '0014_auto_20190823_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='wuspool',
            name='batch_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='WUS Batch'),
        ),
    ]