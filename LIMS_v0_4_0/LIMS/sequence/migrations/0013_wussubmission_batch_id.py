# Generated by Django 2.1.5 on 2019-08-23 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sequence', '0012_auto_20190823_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='wussubmission',
            name='batch_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='wus name2'),
        ),
    ]
