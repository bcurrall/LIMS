# Generated by Django 2.1.5 on 2019-07-16 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0010_sample_sample_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='created',
            field=models.DateField(null=True),
        ),
    ]
