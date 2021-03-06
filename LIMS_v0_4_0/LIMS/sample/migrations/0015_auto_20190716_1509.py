# Generated by Django 2.1.5 on 2019-07-16 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0014_auto_20190716_1201'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sample',
            old_name='archived',
            new_name='stored',
        ),
        migrations.RenameField(
            model_name='sample',
            old_name='status_comments',
            new_name='tracking_comments',
        ),
        migrations.AddField(
            model_name='sample',
            name='stored_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
