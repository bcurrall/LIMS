# Generated by Django 2.1.5 on 2019-07-12 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0009_auto_20190711_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='sample_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]