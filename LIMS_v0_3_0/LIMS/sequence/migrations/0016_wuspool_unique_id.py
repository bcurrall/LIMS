# Generated by Django 2.1.5 on 2019-08-26 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sequence', '0015_wuspool_batch_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='wuspool',
            name='unique_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
