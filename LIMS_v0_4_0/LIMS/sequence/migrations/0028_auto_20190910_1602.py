# Generated by Django 2.1.5 on 2019-09-10 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sequence', '0027_auto_20190904_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wuspool',
            name='num_of_lanes',
            field=models.FloatField(default=0),
        ),
    ]
