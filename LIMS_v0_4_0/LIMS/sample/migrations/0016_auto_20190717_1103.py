# Generated by Django 2.1.5 on 2019-07-17 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0015_auto_20190716_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='created',
            field=models.DateField(blank=True, null=True),
        ),
    ]