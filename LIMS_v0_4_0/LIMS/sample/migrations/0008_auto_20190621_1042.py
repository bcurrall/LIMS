# Generated by Django 2.1.5 on 2019-06-21 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0007_auto_20190620_1715'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sample',
            old_name='freezer_column',
            new_name='rack_column',
        ),
        migrations.RenameField(
            model_name='sample',
            old_name='freezer_row',
            new_name='rack_row',
        ),
    ]
