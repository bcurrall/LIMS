# Generated by Django 2.1.5 on 2019-07-25 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0017_auto_20190717_1201'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sample',
            old_name='sample_id',
            new_name='unique_id',
        ),
    ]
