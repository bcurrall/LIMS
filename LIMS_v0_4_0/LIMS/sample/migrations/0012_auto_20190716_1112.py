# Generated by Django 2.1.5 on 2019-07-16 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0011_sample_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='created',
            field=models.DateField(blank=True, null=True),
        ),
    ]
